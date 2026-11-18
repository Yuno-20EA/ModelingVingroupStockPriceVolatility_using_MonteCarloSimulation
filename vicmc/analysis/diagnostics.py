"""Kiểm định giả thiết GBM: log-return chuẩn, độc lập, phương sai không đổi."""
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Diagnostics:
    skew: float
    excess_kurt: float   # > 0 = đuôi dày
    jb_p: float          # Jarque–Bera: p nhỏ -> không chuẩn
    ac_sq: np.ndarray    # ACF của r² theo độ trễ 1..nlags
    lb_stat: float
    lb_p: float          # Ljung–Box trên r²: p nhỏ -> có cụm biến động
    ac_band: float       # ngưỡng ±1.96/√n


def acf(x: np.ndarray, nlags: int) -> np.ndarray:
    x = x - x.mean()
    return np.array([np.sum(x[k:] * x[:-k]) for k in range(1, nlags + 1)]) / np.sum(x * x)


def run_diagnostics(r: np.ndarray, nlags: int = 20) -> Diagnostics:
    n = len(r)
    ac_sq = acf(r**2, nlags)
    q = n * (n + 2) * np.sum(ac_sq**2 / (n - np.arange(1, nlags + 1)))
    return Diagnostics(float(stats.skew(r)), float(stats.kurtosis(r)), float(stats.jarque_bera(r)[1]),
                       ac_sq, float(q), float(stats.chi2.sf(q, nlags)), float(1.96 / np.sqrt(n)))
