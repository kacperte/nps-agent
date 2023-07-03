import logging
import sys


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level to INFO
        format="%(asctime)s [%(levelname)s] %(message)s",  # Set the logging format
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to standard output
        ],
    )
