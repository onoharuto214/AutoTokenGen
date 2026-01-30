import logging
from typing import Optional
from web3 import Web3
from evmdeploy import compile_solidity, Contract
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ERC20Token:
    """
    ERC20 Token deployer using evmdeploy library.
    Provides a simplified interface for compiling and deploying ERC20 tokens.
    """
    
    def __init__(
        self,
        rpc_url: str,
        private_key: str,
        token_name: str,
        symbol: str,
        dec: int = 18,
        total_supply: int = 0,
        gas_price_gwei: Optional[float] = None,
        solc_version: str = '0.8.0'
    ):
        """
        Initialize the ERC20Token deployer.
        
        Args:
            rpc_url: RPC URL of the blockchain
            private_key: Private key for deployment
            token_name: Name of the token
            symbol: Token symbol
            dec: Token decimals (default: 18)
            total_supply: Total supply (unscaled)
            gas_price_gwei: Optional gas price in Gwei
            solc_version: Solidity compiler version (default: 0.8.0)
        """
        self.contract_path = "./contracts/Token.sol"
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.token_name = token_name
        self.symbol = symbol
        self.dec = int(dec)
        self.total_supply = int(total_supply)
        self.gas_price_gwei = gas_price_gwei
        self.solc_version = solc_version
        
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to RPC at {self.rpc_url}")
        
        # Compile contract
        self.contract = None
        self._compile_contract()
    
    def _compile_contract(self):
        """Compile the Token.sol contract using evmdeploy."""
        logger.info(f"Compiling contract {self.contract_path}...")
        
        try:
            artifacts = compile_solidity(
                path=self.contract_path,
                solc_version=self.solc_version,
                optimizer=True,
                runs=200
            )
            
            # Get the Token contract artifact
            if "Token" not in artifacts:
                raise ValueError("Token contract not found in compiled artifacts")
            
            self.contract = Contract(artifacts["Token"])
            logger.info("Contract compiled successfully")
            
        except FileNotFoundError:
            logger.error(f"Contract file not found at {self.contract_path}")
            raise
        except Exception as e:
            logger.error(f"Compilation failed: {e}")
            raise
    
    def deploy_contract(self) -> Optional[str]:
        """
        Deploy the ERC20 token contract.
        
        Returns:
            Contract address if successful, None otherwise
        """
        logger.info(f"Starting deployment for {self.token_name} ({self.symbol})...")
        
        if not self.contract:
            logger.error("Contract not compiled")
            return None
        
        try:
            # Prepare constructor arguments
            constructor_args = [
                self.token_name,
                self.symbol,
                self.dec,
                self.total_supply
            ]
            
            logger.info(f"Deploying from address: {self.w3.eth.account.from_key(self.private_key).address}")
            
            # Deploy using evmdeploy Contract.deploy()
            # This handles gas estimation, transaction signing, and receipt waiting
            result = self.contract.deploy(
                w3=self.w3,
                private_key=self.private_key,
                constructor_args=constructor_args,
                wait=True
            )
            
            if result.contract_address:
                logger.info(f"Contract deployed successfully at: {result.contract_address}")
                logger.info(f"Transaction Hash: {result.tx_hash}")
                return result.contract_address
            else:
                logger.error("Deployment failed - no contract address returned")
                return None
                
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return None
