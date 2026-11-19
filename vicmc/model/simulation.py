# Lõi mô phỏng Monte Carlo sinh quỹ đạo giá hình học Brown (GBM)
import numpy as np
import pandas as pd

from ..config import DT


def simulate_gbm(s0: float, mu: float, sigma: float, horizon: int,
                 n_paths: int, rng: np.random.Generator) -> np.ndarray:
    # Sinh quỹ đạo GBM theo nghiệm giải tích chính xác, kết hợp biến đối ngẫu (antithetic variates)
    if n_paths % 2:
        raise ValueError("n_paths phải là số chẵn")
    z = rng.standard_normal((n_paths // 2, horizon))
    z = np.vstack([z, -z])
    log_steps = (mu - 0.5 * sigma**2) * DT + sigma * np.sqrt(DT) * z
    paths = s0 * np.exp(np.cumsum(log_steps, axis=1))
    return np.hstack([np.full((n_paths, 1), s0), paths])


def future_dates(last_date: pd.Timestamp, horizon: int) -> pd.DatetimeIndex:
    # Tạo chuỗi ngày làm việc trong tương lai (thứ 2 - thứ 6)
    return pd.bdate_range(last_date + pd.Timedelta(days=1), periods=horizon)
