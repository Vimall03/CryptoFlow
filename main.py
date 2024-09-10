import time
from deposit_processor import fetch_deposits, process_deposits
from ethereum_client import create_web3_instance
import config
import logging_config

logger = logging_config.setup_logging()
web3 = create_web3_instance()  # we are initializing web3 here

def main():
    BLOCK_STEP = config.BLOCK_STEP
    last_checked_block = web3.eth.block_number - BLOCK_STEP

    while True:
        latest_block = web3.eth.block_number
        start_block = hex(last_checked_block + 1)
        end_block = hex(min(latest_block, last_checked_block + BLOCK_STEP))

        logger.info("Fetching deposits from block %s to %s...", start_block, end_block)
        logs = fetch_deposits(start_block, end_block)
        process_deposits(logs)

        last_checked_block += BLOCK_STEP
        if last_checked_block >= latest_block:
            last_checked_block = latest_block - BLOCK_STEP

        time.sleep(60)  # Wait for 1 minute before checking again (trying to implement polling)

if __name__ == "__main__":
    main()
