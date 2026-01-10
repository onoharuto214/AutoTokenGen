import os
import time
import logging
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Install solc version
SOLC_VERSION = '0.8.0'
try:
    install_solc(SOLC_VERSION)
except Exception as e:
    logger.warning(f"Failed to install solc {SOLC_VERSION}: {e}")

def compile_contract(contract_path, contract_name):
    logger.info(f"Compiling contract {contract_path}...")
    try:
        with open(contract_path, 'r') as file:
            contract_source = file.read()
    except FileNotFoundError:
        logger.error(f"Contract file not found at {contract_path}")
        return None

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_name: {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                    }
                }
            }
        },
        solc_version=SOLC_VERSION
    )
    return compiled_sol

class ERC20Token:
    def __init__(self, rpc_url, private_key, token_name, symbol, dec=18, total_supply=0, gas_price_gwei=None):
        self.contract_path = "./contracts/Token.sol"
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.token_name = token_name
        self.symbol = symbol
        self.dec = int(dec)
        self.total_supply = int(total_supply)
        self.gas_price_gwei = gas_price_gwei
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to RPC at {self.rpc_url}")

    def deploy_contract(self):
        logger.info(f"Starting deployment for {self.token_name} ({self.symbol})...")
        
        data = compile_contract(self.contract_path, "Token.sol")
        if not data:
            return None

        abi = data["contracts"]["Token.sol"]["Token"]["abi"]
        bytecode = data["contracts"]["Token.sol"]["Token"]["evm"]["bytecode"]["object"]
        
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        account = self.w3.eth.account.from_key(self.private_key)
        address = account.address

        logger.info(f"Deploying from address: {address}")

        try:
            # Estimate gas
            constructor_txn = contract.constructor(self.token_name, self.symbol, self.dec, self.total_supply)
            gas_estimate = constructor_txn.estimate_gas({'from': address})
            
            # Prepare transaction
            gas_price = self.w3.to_wei(self.gas_price_gwei, 'gwei') if self.gas_price_gwei else self.w3.eth.gas_price
            
            transaction = constructor_txn.build_transaction({
                'from': address,
                'gas': int(gas_estimate * 1.1),  # Add 10% buffer
                'gasPrice': gas_price,
                'nonce': self.w3.eth.get_transaction_count(address),
                'chainId': self.w3.eth.chain_id
            })

            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            logger.info(f"Transaction sent. Hash: {tx_hash.hex()}")
            logger.info("Waiting for confirmation...")

            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
            
            if tx_receipt['status'] == 1:
                logger.info(f"Contract deployed successfully at: {tx_receipt['contractAddress']}")
                return tx_receipt['contractAddress']
            else:
                logger.error("Transaction failed!")
                return None

        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return None

