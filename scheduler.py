import time

from schedule import every
from schedule import repeat
from schedule import run_pending

from src.etl_job import etl_job
from src.logger import logger

TIME_TO_RUN_SCRIPT = 1


@repeat(every(TIME_TO_RUN_SCRIPT).minutes)
def job() -> None:
    logger.info("Running pipeline job")
    etl_job()


logger.info("Starting Manglar")
while True:
    run_pending()
    time.sleep(1)
