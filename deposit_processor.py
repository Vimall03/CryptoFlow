import json
import time
import os
from ethereum_client import create_web3_instance
import config
import logging_config

# Set up logger and create web3 instance
logger = logging_config.setup_logging()
web3 = create_web3_instance()

def fetch_deposits(start_block, end_block):
  # Set filter parameters for fetching logs
  filter_params = {
    'address': config.BEACON_CONTRACT_ADDRESS,
    'fromBlock': start_block,
    'toBlock': end_block,
  }
  
  try:
    # Fetch logs from Ethereum blockchain
    logs = web3.eth.get_logs(filter_params)
    logger.info(f"Fetched {len(logs)} logs from blocks {start_block} to {end_block}.")
    return logs
  except Exception as e:
    # Handle error while fetching logs
    error_message = f"Error fetching logs: {e}"
    logger.error(error_message)
    log_error(error_message)
    return []

def process_deposits(logs):
  new_deposits = []
  for log in logs:
    transaction_hash = log['transactionHash'].hex()
    block_number = log['blockNumber']
    block_timestamp = web3.eth.get_block(block_number)['timestamp']
    
    try:
      # Fetch transaction details for the deposit
      transaction = web3.eth.get_transaction(transaction_hash)
      sender_address = transaction['from']
      amount = float(web3.from_wei(transaction['value'], 'ether'))
    except Exception as e:
      # Handle error while fetching transaction details
      error_message = f"Error fetching transaction details for {transaction_hash}: {e}"
      logger.error(error_message)
      log_error(error_message)
      sender_address = None
      amount = None
    
    # Create deposit information dictionary
    deposit_info = {
      "blockNumber": block_number,
      "blockTimestamp": block_timestamp,
      "fee": amount,
      "hash": transaction_hash,
      "pubkey": sender_address
    }

    new_deposits.append(deposit_info)
    logger.info("Deposit Found:")
    logger.info(f"Block Number: {block_number}")
    logger.info(f"Block Timestamp: {block_timestamp}")
    logger.info(f"Transaction Hash: {transaction_hash}")
    logger.info(f"Sender Address (Pubkey): {sender_address}")
    logger.info(f"Amount (Fee): {amount} Ether")
    logger.info("-" * 40)

  if new_deposits:
    if os.path.exists(config.DEPOSIT_LOG_FILE):
      with open(config.DEPOSIT_LOG_FILE, 'r') as file:
        try:
          existing_data = json.load(file)
        except json.JSONDecodeError:
          existing_data = []
    else:
      existing_data = []

    existing_data.extend(new_deposits)

    with open(config.DEPOSIT_LOG_FILE, 'w') as file:
      json.dump(existing_data, file, indent=4)
    
    logger.info(f"Updated {config.DEPOSIT_LOG_FILE} with {len(new_deposits)} new deposits.")
  else:
    logger.info("No new deposits found in the fetched logs.")

def log_error(message):
  error_entry = {
    "timestamp": time.time(),
    "error_message": message
  }
#21BCE10949
  if os.path.exists(config.ERROR_LOG_FILE):
    with open(config.ERROR_LOG_FILE, 'r') as file:
      try:
        error_data = json.load(file)
      except json.JSONDecodeError:
        error_data = []
  else:
    error_data = []

  error_data.append(error_entry)

  with open(config.ERROR_LOG_FILE, 'w') as file:
    json.dump(error_data, file, indent=4)
