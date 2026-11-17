"""Hằng số và tham số chạy."""
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRADING_DAYS = 252           # số phiên giao dịch mỗi năm
DT = 1 / TRADING_DAYS        # một phiên, tính theo năm


@dataclass(frozen=True)
class Config:
    data_path: Path = ROOT / "data" / "raw" / "VIC_2022-11-16_2026-11-16.csv"
    data_start: str | None = None    # None = từ phiên đầu tiên trong file
    data_end: str | None = None      # None = đến phiên cuối cùng
    calib_days: int = 250            # cửa sổ ước lượng μ, σ (~1 năm)
    horizon: int = 60                # số phiên dự báo (~3 tháng)
    n_paths: int = 10_000            # số quỹ đạo Monte Carlo (chẵn)
    seed: int = 42
    bt_horizon: int = 20             # backtest: dự báo trước 20 phiên
    bt_step: int = 10                # backtest: cách nhau 10 phiên
    bt_paths: int = 2_000            # backtest: số quỹ đạo mỗi mốc
    out_dir: Path = ROOT / "outputs"
