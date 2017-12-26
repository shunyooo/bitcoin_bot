import api
import pandas as pd
from time import sleep
from config import config
from logger import get_module_logger
from db import engine
import slack
import traceback
logger = get_module_logger(__name__)
SPAN_SEC = int(config["collect_data"]["SPAN_SEC"])
AUTO_COLLECT = bool(config["collect_data"]["AUTO_COLLECT"])


def fetch_ticker():
    # ticker情報を取得する。
    ticker = api.bitflyer.ticker(product_code="BTC_JPY")
    return pd.DataFrame([ticker])


def main():
    slack.post("データ収集を開始します。→{}".format(engine.url), color="good")
    # SPAN_SEC 毎にtickerを取得して、DBに貯める。
    # TODO: 何時間か毎にslackに収集状況の通知を行うように。
    while(True):
        sleep(SPAN_SEC)
        try:
            ticker = fetch_ticker()
            ticker.to_sql(name="ticker", con=engine, if_exists="append")
            logger.debug("fetch_ticker ltp:{} span:{}".format(
                ticker.ltp, SPAN_SEC))
        except Exception as e:
            traceback_str = traceback.format_exc()
            info = "{}\n{}".format(str(e), traceback_str)
            slack.post(info, color="danger")

if __name__ == '__main__':
    if AUTO_COLLECT:
        logger.debug("データ収集プログラムを起動します。")
        main()
    else:
        logger.debug("データ収集プログラムは起動しません。")
