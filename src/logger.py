import logging

LOGGING_FILE = "app.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOGGING_FILE)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
