# Đo lường các chỉ số rủi ro (VaR, CVaR, xác suất) từ phân phối giá cuối kỳ
from dataclasses import dataclass

import numpy as np

from ..config import DT

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]


@dataclass(frozen=True)
class RiskMetrics:
    s0: float
    mean_mc: float
    mean_theory: float     # Kỳ vọng lý thuyết: E[S_T] = S0 * e^{μT}
    median_mc: float
    median_theory: float   # Trung vị lý thuyết: S0 * e^{(μ - σ²/2)T}
    q05: float
    q95: float
    var95: float           # VaR 95%: mức tổn thất tối đa ở độ tin cậy 95%
    cvar95: float          # CVaR 95%: kỳ vọng tổn thất trung bình trong 5% xấu nhất
    p_profit: float        # Xác suất sinh lời P(S_T > S0)
    p_loss_10: float       # Xác suất lỗ trên 10%
    p_gain_20: float       # Xác suất lãi trên 20%


def risk_metrics(paths: np.ndarray, mu: float, sigma: float) -> RiskMetrics:
    # Tính toán toàn bộ các thước đo thống kê và rủi ro từ ma trận quỹ đạo
    T = (paths.shape[1] - 1) * DT
    s0, st = float(paths[0, 0]), paths[:, -1]
    ret = st / s0 - 1.0
    q05 = float(np.quantile(ret, 0.05))
    return RiskMetrics(
        s0=s0, mean_mc=float(st.mean()), mean_theory=s0 * float(np.exp(mu * T)),
        median_mc=float(np.median(st)), median_theory=s0 * float(np.exp((mu - 0.5 * sigma**2) * T)),
        q05=float(np.quantile(st, 0.05)), q95=float(np.quantile(st, 0.95)),
        var95=-q05, cvar95=-float(ret[ret <= q05].mean()),
        p_profit=float((st > s0).mean()), p_loss_10=float((ret < -0.10).mean()),
        p_gain_20=float((ret > 0.20).mean()))


def quantile_paths(paths: np.ndarray) -> np.ndarray:
    # Trích xuất các dải phân vị theo thời gian để vẽ đồ thị hình quạt (fan chart)
    return np.quantile(paths, LEVELS, axis=0)
