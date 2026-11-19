# Kiểm tra tính toàn vẹn và chất lượng dữ liệu lịch sử
from dataclasses import dataclass

import numpy as np
import pandas as pd

LIMIT = 0.07   # Biên độ trần/sàn ±7% của sàn HOSE


@dataclass(frozen=True)
class DataQuality:
    n_obs: int
    start: pd.Timestamp
    end: pd.Timestamp
    min_close: float
    max_close: float
    total_growth_x: float
    n_long_gaps: int           # Số khoảng trống > 4 ngày (nghỉ lễ/Tết)
    max_gap_days: int
    max_abs_logret: float
    n_near_limit: int          # Số phiên chạm biên ±7%
    n_src_mismatch: int | None # Số phiên lệch giữa % thay đổi nguồn và giá tự tính


def check_quality(df: pd.DataFrame) -> DataQuality:
    close = df["close"]
    r = np.log(close).diff().dropna()
    gaps = df.index.to_series().diff().dt.days.dropna()
    mismatch = None
    if "src_pct" in df:   # Kiểm tra điều chỉnh sau cổ tức/chia tách
        mismatch = int(((df["src_pct"] - close.pct_change() * 100).abs().iloc[1:] > 0.1).sum())
    return DataQuality(
        n_obs=len(df), start=df.index[0], end=df.index[-1],
        min_close=float(close.min()), max_close=float(close.max()),
        total_growth_x=float(close.iloc[-1] / close.iloc[0]),
        n_long_gaps=int((gaps > 4).sum()), max_gap_days=int(gaps.max()),
        max_abs_logret=float(r.abs().max()),
        n_near_limit=int((np.expm1(r).abs() > LIMIT * 0.93).sum()),
        n_src_mismatch=mismatch)
