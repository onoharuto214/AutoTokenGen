
# AutoTokenGen - Automatic ERC-20 Token Generator

AutoTokenGen is a Python program that simplifies the process of creating and deploying ERC-20 tokens on Any EVM blockchain. With customizable parameters, you can effortlessly generate your own tokens for various use cases.

## Features

- **Easy Customization:** Modify parameters such as token name, symbol, initial supply, and more to create a token tailored to your needs.

- **Automatic Deployment:** The program automates the deployment process, saving you time and effort.

- **Web3.py Integration:** Utilizes the Web3.py library for seamless interaction with the blockchain.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3
- [Web3.py](https://web3py.readthedocs.io/en/stable/)
- py-solc-x

### Usage

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/rakibmia7254/AutoTokenGen.git
   cd AutoTokenGen
   ```
   2.Customize the token parameters in the `main.py` file:
   ```python
   import  deploy
   contract_deployer  =  deploy.ERC20Token(
	   rpc_url="https://data-seed-prebsc-1-s3.binance.org:8545/",
	   gasPrice=5,
	   private_key="your_private_key",
	   token_name='TestToken',
	   symbol='Test',
	   total_supply=10000000000,
	   dec=18
   )
   print(contract_deployer.deploy_contract())```


3.Run the program:
```bash
python main.py
```
it will print your deployed contract address


### License
This project is licensed under the MIT License - see the LICENSE file for details

#### Author:
1. Rakib Hossain
