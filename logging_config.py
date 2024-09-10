import logging
import os

def setup_logging():
    # Ensure the logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    log_file = 'logs/deposit_processor.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Optional: also log to console
        ]
    )
    return logging.getLogger(__name__)
