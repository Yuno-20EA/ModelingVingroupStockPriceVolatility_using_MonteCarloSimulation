"""Đọc tham số dòng lệnh thành Config."""
import argparse
from pathlib import Path

from .config import Config


def parse_args(argv: list[str] | None = None) -> Config:
    d = Config()
    ap = argparse.ArgumentParser(description="Monte Carlo GBM cho cổ phiếu VIC")
    ap.add_argument("--data", type=Path, default=d.data_path, help="file CSV giá")
    ap.add_argument("--start", default=d.data_start, help="ngày bắt đầu YYYY-MM-DD")
    ap.add_argument("--end", default=d.data_end, help="ngày kết thúc YYYY-MM-DD")
    ap.add_argument("--calib-days", type=int, default=d.calib_days)
    ap.add_argument("--horizon", type=int, default=d.horizon)
    ap.add_argument("--paths", type=int, default=d.n_paths)
    ap.add_argument("--seed", type=int, default=d.seed)
    ap.add_argument("--bt-horizon", type=int, default=d.bt_horizon)
    ap.add_argument("--bt-step", type=int, default=d.bt_step)
    ap.add_argument("--out", type=Path, default=d.out_dir)
    a = ap.parse_args(argv)
    return Config(data_path=a.data, data_start=a.start, data_end=a.end, calib_days=a.calib_days,
                  horizon=a.horizon, n_paths=a.paths + a.paths % 2,   # số chẵn cho biến đối ngẫu
                  seed=a.seed, bt_horizon=a.bt_horizon, bt_step=a.bt_step, out_dir=a.out)
