import api
import pandas as pd
from time import sleep
from config import config
from logger import get_module_logger
from db import engine
logger = get_module_logger(__name__)
SPAN_SEC = int(config["collect_data"]["SPAN_SEC"])
AUTO_COLLECT = bool(config["collect_data"]["AUTO_COLLECT"])


def fetch_ticker():
    # ticker情報を取得する。
    ticker = api.bitflyer.ticker(product_code="BTC_JPY")
    return pd.DataFrame([ticker])


def main():
    while(True):
        sleep(SPAN_SEC)
        ticker = fetch_ticker()
        ticker.to_sql(name="ticker", con=engine, if_exists="append")
        logger.debug("fetch_ticker ltp:{} span:{}".format(
            ticker.ltp, SPAN_SEC))

if __name__ == '__main__':
    if AUTO_COLLECT:
        main()
