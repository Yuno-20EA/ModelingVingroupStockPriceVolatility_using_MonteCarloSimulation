# Kiểm định các giả thiết thống kê của mô hình GBM (chuẩn, độc lập, đuôi dày)
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Diagnostics:
    skew: float          # Độ lệch (Skewness)
    excess_kurt: float   # Độ nhọn dư (Excess Kurtosis > 0 biểu thị đuôi dày)
    jb_p: float          # p-value kiểm định phân phối chuẩn Jarque-Bera
    ac_sq: np.ndarray    # Hàm tự tương quan (ACF) của r²
    lb_stat: float       # Thống kê Ljung-Box trên r²
    lb_p: float          # p-value Ljung-Box (p < 0.05 biểu thị cụm biến động)
    ac_band: float       # Dải tin cậy 95% (±1.96/√n)


def acf(x: np.ndarray, nlags: int) -> np.ndarray:
    # Tính hệ số tự tương quan mẫu đến độ trễ nlags
    x = x - x.mean()
    return np.array([np.sum(x[k:] * x[:-k]) for k in range(1, nlags + 1)]) / np.sum(x * x)


def run_diagnostics(r: np.ndarray, nlags: int = 20) -> Diagnostics:
    # Thực hiện kiểm định chuẩn (JB) và kiểm định tự tương quan chuỗi bình phương (LB)
    n = len(r)
    ac_sq = acf(r**2, nlags)
    q = n * (n + 2) * np.sum(ac_sq**2 / (n - np.arange(1, nlags + 1)))
    return Diagnostics(float(stats.skew(r)), float(stats.kurtosis(r)), float(stats.jarque_bera(r)[1]),
                       ac_sq, float(q), float(stats.chi2.sf(q, nlags)), float(1.96 / np.sqrt(n)))
