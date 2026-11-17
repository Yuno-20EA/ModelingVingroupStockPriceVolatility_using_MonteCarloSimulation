"""Lõi Monte Carlo: sinh quỹ đạo giá GBM."""
import numpy as np
import pandas as pd

from ..config import DT


def simulate_gbm(s0: float, mu: float, sigma: float, horizon: int,
                 n_paths: int, rng: np.random.Generator) -> np.ndarray:
    """Nghiệm chính xác:  S_{t+dt} = S_t · exp[(μ − σ²/2)dt + σ√dt · Z],  Z ~ N(0,1).

    Dùng biến đối ngẫu (mỗi Z kèm −Z). Trả về mảng (n_paths, horizon+1); cột 0 là S0.
    """
    if n_paths % 2:
        raise ValueError("n_paths phải là số chẵn")
    z = rng.standard_normal((n_paths // 2, horizon))
    z = np.vstack([z, -z])
    log_steps = (mu - 0.5 * sigma**2) * DT + sigma * np.sqrt(DT) * z
    paths = s0 * np.exp(np.cumsum(log_steps, axis=1))
    return np.hstack([np.full((n_paths, 1), s0), paths])


def future_dates(last_date: pd.Timestamp, horizon: int) -> pd.DatetimeIndex:
    """Các ngày thứ 2–6 kế tiếp (chưa trừ ngày lễ Việt Nam)."""
    return pd.bdate_range(last_date + pd.Timedelta(days=1), periods=horizon)
