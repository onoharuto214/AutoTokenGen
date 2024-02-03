import deploy

contract_deployer = deploy.ERC20Token(
    rpc_url="https://data-seed-prebsc-1-s3.binance.org:8545/",
    gasPrice=5,
    private_key="your_private_key",
    token_name='TestToken',
    symbol='Test',
    total_supply=10000000000,
    dec=18
)
print(contract_deployer.deploy_contract())