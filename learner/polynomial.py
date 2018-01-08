# 1次元の多項式による近似曲線を求めるもの。
import numpy as np
from logger import get_module_logger
logger = get_module_logger(__name__)


def polyfit(x, y, deg):
    """
    Summary: 近似曲線と、その勾配のコールバックを返却。
    Attributes: 
        @param (x):np.array
        @param (y):np.array
        @param (deg):近似多項式の次数
    Returns: poly, grad
    """
    x_mean = x.mean()
    x_max = x.max()
    x_min = x.min()

    # fitting が上手くいくように、平均で引いておく。
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.polyfit.html
    # の Notes より。
    x_ = x - x_mean
    weights = np.polyfit(x_, y, deg).flatten()

    def check_valid(x):
        if x < x_min or x_max < x:
            logger.warning("{}は学習データ範囲[{},{}]外です。".format(x, x_min, x_max))

    def poly(x):
        # 近似曲線
        check_valid(x)
        return np.poly1d(weights)(x - x_mean)

    def grad(x):
        # 近似曲線の勾配
        check_valid(x)
        return np.poly1d(weights).deriv()(x - x_mean)

    return poly, grad
