"""Ghi bảng số liệu ra CSV."""
from pathlib import Path

import numpy as np
import pandas as pd

from ..analysis.risk import quantile_paths


def save_forecast(paths: np.ndarray, dates: pd.DatetimeIndex, out: Path) -> None:
    qs = quantile_paths(paths)
    pd.DataFrame({"date": dates, "q05": qs[0], "q25": qs[1], "q50": qs[2], "q75": qs[3],
                  "q95": qs[4], "mean": paths.mean(axis=0)}).to_csv(out, index=False)


def save_backtest(bt: pd.DataFrame, out: Path) -> None:
    bt.to_csv(out, index=False)
