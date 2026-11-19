# Xuất kết quả dự báo và backtest ra định dạng CSV
from pathlib import Path

import numpy as np
import pandas as pd

from ..analysis.risk import quantile_paths


def save_forecast(paths: np.ndarray, dates: pd.DatetimeIndex, out: Path) -> None:
    # Lưu chuỗi phân vị dự báo theo từng phiên ra file CSV
    qs = quantile_paths(paths)
    pd.DataFrame({"date": dates, "q05": qs[0], "q25": qs[1], "q50": qs[2], "q75": qs[3],
                  "q95": qs[4], "mean": paths.mean(axis=0)}).to_csv(out, index=False)


def save_backtest(bt: pd.DataFrame, out: Path) -> None:
    # Lưu toàn bộ chi tiết các mốc kiểm định backtest ra file CSV
    bt.to_csv(out, index=False)
