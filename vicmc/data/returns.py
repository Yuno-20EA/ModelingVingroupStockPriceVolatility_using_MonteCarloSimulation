# Chuyển đổi chuỗi giá sang chuỗi lợi suất logarit (log-returns)
import numpy as np
import pandas as pd


def log_returns(prices: pd.Series) -> np.ndarray:
    # Tính r_t = ln(S_t / S_{t-1})
    return np.log(prices).diff().dropna().values
