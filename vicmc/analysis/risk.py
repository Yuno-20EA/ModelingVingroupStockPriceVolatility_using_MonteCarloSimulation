"""Chỉ số rủi ro từ phân phối giá cuối kỳ của các quỹ đạo Monte Carlo."""
from dataclasses import dataclass

import numpy as np

from ..config import DT

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]


@dataclass(frozen=True)
class RiskMetrics:
    s0: float
    mean_mc: float
    mean_theory: float     # E[S_T] = S0·e^{μT}
    median_mc: float
    median_theory: float   # S0·e^{(μ−σ²/2)T}
    q05: float
    q95: float
    var95: float           # −q_5%(R): tổn thất vượt ngưỡng với xác suất 5%
    cvar95: float          # −E[R | R ≤ q_5%]: tổn thất trung bình trong 5% xấu nhất
    p_profit: float
    p_loss_10: float
    p_gain_20: float


def risk_metrics(paths: np.ndarray, mu: float, sigma: float) -> RiskMetrics:
    T = (paths.shape[1] - 1) * DT
    s0, st = float(paths[0, 0]), paths[:, -1]
    ret = st / s0 - 1.0                      # lợi suất cả kỳ R
    q05 = float(np.quantile(ret, 0.05))
    return RiskMetrics(
        s0=s0, mean_mc=float(st.mean()), mean_theory=s0 * float(np.exp(mu * T)),
        median_mc=float(np.median(st)), median_theory=s0 * float(np.exp((mu - 0.5 * sigma**2) * T)),
        q05=float(np.quantile(st, 0.05)), q95=float(np.quantile(st, 0.95)),
        var95=-q05, cvar95=-float(ret[ret <= q05].mean()),
        p_profit=float((st > s0).mean()), p_loss_10=float((ret < -0.10).mean()),
        p_gain_20=float((ret > 0.20).mean()))


def quantile_paths(paths: np.ndarray) -> np.ndarray:
    """Phân vị 5/25/50/75/95% tại từng bước -> shape (5, horizon+1)."""
    return np.quantile(paths, LEVELS, axis=0)
