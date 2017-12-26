import pandas as pd
import datetime
from .utils import engine


def filter_by_date(df, from_date, to_date):
    # 時期で絞る
    return df.ix[from_date, to_date]


def max_timestamp(table):
    # 最大時間の取得。文字列で返却。%Y-%m-%dT%H:%M:%S.%f
    q = "SELECT MAX(timestamp) FROM {}".format(table)
    max_t = engine.execute(q).first()[0]
    return max_t


def gen_query(table, start=None, end=None):
    # クエリの発行。timestampでWHERE対応。
    q = "SELECT * FROM {} ".format(table)
    should_where = True

    def add_op_if_needed():
        nonlocal should_where
        nonlocal q
        if should_where:
            q += "WHERE "
            should_where = False
        else:
            q += "AND "

    if isinstance(start, str):
        add_op_if_needed()
        q += "timestamp >= '{}' ".format(start)
    if isinstance(end, str):
        add_op_if_needed()
        q += "timestamp <= '{}' ".format(end)
    return q


def read_ticker(start=None, end=None, sec_by=None):
    """
    Summary: plot_ltp
    Attributes: 
        @param (start) default=None: 開始時間。文字列。   
        @param (end) default=None: 終端時間。文字列。
        @param (sec_by) default=None: 終端時間から、何秒前までのデータを取るか。startとの兼用は不可。
    """
    assert not((start is not None) and (
        sec_by is not None)), "start と sec_by は兼用不可です。"

    table = "ticker"

    # TODO:SQLから抽出を行う。なぜか日付による抽出がうまく行かないので、保留。
    # if sec_by is not None:
    #     if end is None:
    #         # 終端時間の取得
    #         max_time = max_timestamp(table)
    #         end = datetime.datetime.strptime(max_time, "%Y-%m-%dT%H:%M:%S.%f")
    #     end_by = end - datetime.timedelta(seconds=sec_by)
    #     start = end_by.strftime('%Y-%m-%d %H:%M:%S')

    query = gen_query(table)
    t_df = pd.read_sql(query, engine,
                       parse_dates=["timestamp"],
                       index_col=["timestamp"])
    if sec_by is not None:
        # 終端時間からの秒数で指定。
        end_by = t_df.index.max() - datetime.timedelta(seconds=sec_by)
        end_by = end_by.strftime('%Y-%m-%d %H:%M:%S')
        t_df = t_df.loc[end_by:]

    return t_df
