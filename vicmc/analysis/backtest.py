# Kiểm định mô hình bằng phương pháp Backtest cuốn chiếu (Rolling Backtest)
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from ..model.estimation import estimate_gbm
from ..model.simulation import simulate_gbm


@dataclass(frozen=True)
class BacktestSummary:
    n_origins: int
    coverage_90: float   # Tỷ lệ giá thực tế nằm trong khoảng 90% (lý tưởng: 90%)
    coverage_50: float   # Tỷ lệ giá thực tế nằm trong khoảng 50% (lý tưởng: 50%)
    below_q05: float     # Tỷ lệ giá thực tế thấp hơn phân vị 5% (lý tưởng: 5%)
    above_q95: float     # Tỷ lệ giá thực tế vượt phân vị 95% (lý tưởng: 5%)
    mape_median: float   # Sai số MAPE giữa trung vị dự báo và giá thực tế
    ks_stat: float       # Thống kê kiểm định Kolmogorov-Smirnov trên PIT
    ks_p: float          # p-value kiểm định phân phối đều PIT ~ U(0,1)


def rolling_backtest(prices: pd.Series, calib_days: int, horizon: int, step: int,
                     n_paths: int, drift_mode: str, seed: int) -> pd.DataFrame:
    # Dự báo trượt out-of-sample tại từng mốc i và so sánh với giá thực tế tại i + horizon
    if drift_mode not in ("estimated", "zero"):
        raise ValueError("drift_mode phải là 'estimated' hoặc 'zero'")
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(calib_days, len(prices) - horizon, step):
        p = estimate_gbm(prices.iloc[i - calib_days: i + 1])
        mu = p.mu if drift_mode == "estimated" else 0.0
        st = simulate_gbm(prices.iloc[i], mu, p.sigma, horizon, n_paths, rng)[:, -1]
        actual = prices.iloc[i + horizon]
        q = np.quantile(st, [0.05, 0.25, 0.5, 0.75, 0.95])
        rows.append({"origin": prices.index[i], "target": prices.index[i + horizon],
                     "s0": prices.iloc[i], "actual": actual,
                     "q05": q[0], "q25": q[1], "q50": q[2], "q75": q[3], "q95": q[4],
                     "pit": float((st < actual).mean()), "mu": mu, "sigma": p.sigma})
    return pd.DataFrame(rows)


def summarize_backtest(bt: pd.DataFrame) -> BacktestSummary:
    # Tính các chỉ số đánh giá độ chuẩn xác dự báo và kiểm định PIT
    ks = stats.kstest(bt["pit"], "uniform")
    return BacktestSummary(
        len(bt), float(((bt.actual >= bt.q05) & (bt.actual <= bt.q95)).mean()),
        float(((bt.actual >= bt.q25) & (bt.actual <= bt.q75)).mean()),
        float((bt.actual < bt.q05).mean()), float((bt.actual > bt.q95).mean()),
        float((np.abs(bt.q50 - bt.actual) / bt.actual).mean()), float(ks.statistic), float(ks.pvalue))
