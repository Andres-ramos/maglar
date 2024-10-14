import time

from schedule import every
from schedule import repeat
from schedule import run_pending

from src.etl_job import etl_job


@repeat(every(1).minutes)
def job() -> None:
    etl_job()


while True:
    run_pending()
    time.sleep(1)
