# dbから読み取る系。
from db import df
import matplotlib
from .plot import plot


def plot_ltp(figsize=(16, 10), start=None, end=None, sec_by=None):
    """
    Summary: plot_ltp
    Attributes: 
        @param (start) default=None: 開始時間。文字列。   
        @param (end) default=None: 終端時間。文字列。
        @param (sec_by) default=None: 終端時間から、何秒前までのデータを取るか。
    """
    ltp = df.read_ticker(start=start, end=end, sec_by=sec_by)[["ltp"]]
    plot(figsize=figsize)
    return ltp
