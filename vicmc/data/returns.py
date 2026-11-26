# Chuỗi giá -> chuỗi log-return
import numpy as np
import pandas as pd


def log_returns(prices: pd.Series) -> np.ndarray:
    # r_t = ln(S_t / S_{t-1}): cộng được theo thời gian, GBM giả định r_t ~ chuẩn
    return np.log(prices).diff().dropna().values
