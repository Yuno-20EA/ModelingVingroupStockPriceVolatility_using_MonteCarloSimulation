# Ước lượng tham số (μ, σ) cho mô hình GBM theo phương pháp MLE
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..config import DT
from ..data.returns import log_returns


@dataclass(frozen=True)
class GBMParams:
    n_returns: int
    mu: float        # Độ trôi quy năm (/năm)
    sigma: float     # Độ biến động quy năm (/năm)
    se_mu: float     # Sai số chuẩn của μ̂
    start: pd.Timestamp
    end: pd.Timestamp


def estimate_gbm(prices: pd.Series) -> GBMParams:
    # Ước lượng MLE: σ̂ = std(r)/√dt, μ̂ = mean(r)/dt + σ̂²/2, SE(μ̂) ≈ σ/√T
    r = log_returns(prices)
    sigma = r.std(ddof=1) / np.sqrt(DT)
    mu = r.mean() / DT + 0.5 * sigma**2
    return GBMParams(len(r), mu, sigma, sigma / np.sqrt(len(r) * DT), prices.index[0], prices.index[-1])


def rolling_estimates(prices: pd.Series, window: int) -> pd.DataFrame:
    # Tính (μ̂, σ̂) trên cửa sổ trượt để kiểm tra tính ổn định theo thời gian
    r = np.log(prices).diff().dropna()
    sigma = r.rolling(window).std() / np.sqrt(DT)
    return pd.DataFrame({"mu": r.rolling(window).mean() / DT + 0.5 * sigma**2, "sigma": sigma}).dropna()
