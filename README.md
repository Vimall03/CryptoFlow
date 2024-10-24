# CryptoFlow:  Monitoring and logging Ethereum deposits

I’ve written a script to track Ethereum deposits and log them. Here’s how everything works and how to get it up and running.

## How It Works

### 1. Configuration File (`config.py`)
This file holds all the settings for the script. Here’s what you’ll find:
- **ALCHEMY_URL**: The URL for connecting to Ethereum through Alchemy.
- **BEACON_CONTRACT_ADDRESS**: The address of the Beacon Deposit Contract on Ethereum.
- **DEPOSIT_LOG_FILE**: Path to the file where deposit logs are stored.
- **ERROR_LOG_FILE**: Path to the file where errors are logged.
- **BLOCK_STEP**: Number of blocks to check in each batch.

### 2. Main Script (`main.py`)
This is the core of the project. Here’s what it does:
- **Sets Up Logging**: Configures how logs are handled to keep track of events and errors.
- **Creates Web3 Instance**: Initializes the connection to the Ethereum network using Web3.
- **Fetches and Processes Deposits**: Retrieves deposit logs, processes them, and updates the deposit log file.

### 3. Deposit Processor (`deposit_processor.py`)
In this module:
- **Fetching Deposits**: Handles pulling deposit logs from the Ethereum blockchain.
- **Processing Deposits**: Extracts relevant details from the logs and updates the deposit log file. It also handles any errors that may occur.

### 4. Logging Setup
I’ve set up logging to be organized:
- **Deposit Logs**: Deposit details are saved in `logs/deposit_logs.json`.
- **Error Logs**: Errors are recorded in `logs/error_logs.json`.

## Getting Started

1. **Install Dependencies**: Create a `requirements.txt` file with the following and run `pip install -r requirements.txt` to install the necessary packages:
    ```makefile
    web3==6.0.0
    requests==2.28.1
    ```

2. **Set Up Configuration**: Fill out the `config.py` file with your own Alchemy API key, and tweak any other required settings.

3. **Run the Script**: Execute `python main.py` to start monitoring Ethereum deposits. The script will continuously check for new deposits and update the log file accordingly.

## Docker

This project is dockerized. You can build and run the Docker container with the following commands:

- **Build the Docker Image**:
    ```bash
    docker build -t ethereum-deposit-tracker .
    ```

- **Run the Docker Container**:
    ```bash
    docker run -d --name deposit-tracker ethereum-deposit-tracker
    ```

## Future Goals

The future goal is to set up a Telegram bot to send notifications about new deposits. This can be done using the BotFather bot in Telegram to create a new bot and obtain the bot token. Once the bot is created, you can use the Telegram account ID to send messages to the specified account.



