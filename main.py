import os
import argparse
import deploy
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AutoTokenGen - Deploy ERC-20 Tokens")
    
    # Provider & Security
    parser.add_argument("--rpc", help="RPC URL of the blockchain", default=os.getenv("RPC_URL"))
    parser.add_argument("--key", help="Private Key for deployment", default=os.getenv("PRIVATE_KEY"))
    
    # Token Details
    parser.add_argument("--name", help="Token Name", default=os.getenv("TOKEN_NAME", "MyToken"))
    parser.add_argument("--symbol", help="Token Symbol", default=os.getenv("TOKEN_SYMBOL", "MTK"))
    parser.add_argument("--decimals", type=int, help="Token Decimals", default=int(os.getenv("TOKEN_DECIMALS", 18)))
    parser.add_argument("--supply", type=int, help="Total Supply (unscaled)", default=int(os.getenv("TOKEN_SUPPLY", 1000000)))
    
    # Transaction Params
    parser.add_argument("--gas", type=float, help="Gas price in Gwei (optional)", default=os.getenv("GAS_PRICE_GWEI"))

    args = parser.parse_args()

    # Validate required inputs
    if not args.rpc:
        print("Error: RPC URL is required. Provide --rpc or set RPC_URL in .env")
        return
    if not args.key or args.key == "your_private_key":
        print("Error: Private key is required. Provide --key or set PRIVATE_KEY in .env")
        return

    # Initialize deployer
    contract_deployer = deploy.ERC20Token(
        rpc_url=args.rpc,
        private_key=args.key,
        token_name=args.name,
        symbol=args.symbol,
        dec=args.decimals,
        total_supply=args.supply,
        gas_price_gwei=args.gas
    )

    address = contract_deployer.deploy_contract()
    if address:
        print(f"\nSUCCESS: Token deployed at {address}")
    else:
        print("\nFAILED: Deployment was unsuccessful.")

if __name__ == "__main__":
    main()