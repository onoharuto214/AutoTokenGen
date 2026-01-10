# AutoTokenGen - Automatic ERC-20 Token Generator

AutoTokenGen is a modern Python CLI tool that simplifies the process of creating and deploying ERC-20 tokens on any EVM-compatible blockchain.

## Features

- **CLI-Driven:** Easily specify token parameters via command-line arguments.
- **Environment Support:** Securely manage private keys and RPC URLs using `.env` files.
- **Modern Smart Contracts:** Uses Solidity 0.8.x for better security and efficiency.
- **Automatic Deployment:** Handles compilation, gas estimation, and deployment in one go.
- **Logging:** Detailed logging for every step of the deployment process.

## Getting Started

### Prerequisites

- Python 3.8+
- [web3.py](https://web3py.readthedocs.io/)
- [py-solc-x](https://github.com/crytic/py-solc-x)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rakibmia7254/AutoTokenGen.git
   cd AutoTokenGen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables (recommended):
   ```bash
   cp .env.example .env
   # Edit .env with your private key and RPC URL
   ```

### Usage

You can deploy a token using either environment variables or CLI arguments.

**Using CLI arguments:**
```bash
python main.py --rpc YOUR_RPC_URL --key YOUR_PRIVATE_KEY --name "MyToken" --symbol "MTK" --supply 1000000
```

**Using .env file:**
If your `.env` is configured, simply run:
```bash
python main.py
```

### Security Warning
> [!CAUTION]
> Never share your private key or commit your `.env` file to a public repository. Ensure `.env` is listed in your `.gitignore`.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

#### Author:
1. Rakib Hossain
