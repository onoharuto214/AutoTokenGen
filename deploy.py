from web3 import Web3
from solcx import compile_standard, install_solc
import time
install_solc('0.8.0')


blockchain_rpc_urls = {
    "Ethereum": {
        "mainnet": "https://mainnet.ethereum.org",
        "testnet": "https://ropsten.ethereum.org"
    },
    "BNB": {
        "mainnet": "https://bsc-dataseed.binance.org/",
        "testnet": "https://data-seed-prebsc-1-s1.binance.org:8545/"
    },
    "Avalanche": {
        "testnet": "https://api.avax-test.network/ext/bc/C/rpc"
    },
    "Polygon": {
        "testnet": "https://rpc-mumbai.matic.today",
        "mainnet": "https://rpc-mainnet.matic.network"
    }
}

def compile_contract(contract_path, contract):
    with open(contract_path, 'r') as file:
        contract_source = file.read()
    compiled_sol = compile_standard(
        {
              "language": "Solidity",
             "sources": {contract: {"content": contract_source}},
            "settings": {
                   "outputSelection": {
                      "*": {
                         "*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                       }
                }
             }
         },
        solc_version="0.8.0"
    )
    return compiled_sol

class ERC20Token:
    def __init__(self, rpc_url, gasPrice, private_key, token_name, symbol, dec=18, total_supply=0):
        self.contract_path = "./contracts/Token.sol"
        self.gasPrice = gasPrice
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.token_name = token_name
        self.symbol = symbol
        self.dec = dec
        self.total_supply = total_supply

    def deploy_contract(self):

        data=compile_contract(self.contract_path,"Token.sol")

        w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        contract = w3.eth.contract(
            abi=data["contracts"]["Token.sol"]["Token"]["abi"],
            bytecode=data["contracts"]["Token.sol"]["Token"]["evm"]["bytecode"]["object"]
        )

        gas_estimate = contract.constructor(self.token_name, self.symbol, self.dec, self.total_supply).estimate_gas()

        transaction = contract.constructor(self.token_name, self.symbol, self.dec, self.total_supply).build_transaction({
            'from': w3.eth.account.from_key(self.private_key).address,
            'gas': gas_estimate,
            'gasPrice': w3.to_wei(self.gasPrice, 'gwei'),
            'nonce': w3.eth.get_transaction_count(w3.eth.account.from_key(self.private_key).address)
        })

        signed_transaction = w3.eth.account.sign_transaction(transaction, self.private_key)

        try:
            tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        except ValueError as ve:
            print(f"Error: {ve}")
            exit()

        time.sleep(3)
        transaction_receipt = None
        while transaction_receipt is None:
            try:
                transaction_receipt = w3.eth.get_transaction_receipt(tx_hash)
            except:
                pass
            if transaction_receipt is None:
                return {"Waiting for the transaction to be mined..."}
            else:
                return {"Contract address": transaction_receipt['contractAddress']}

