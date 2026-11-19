# Cấu hình tham số và hằng số toàn dự án
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRADING_DAYS = 252           # Số phiên giao dịch/năm
DT = 1 / TRADING_DAYS        # Quy đổi 1 phiên sang năm


@dataclass(frozen=True)
class Config:
    data_path: Path = ROOT / "data" / "raw" / "VIC_2022-11-16_2026-11-16.csv"
    data_start: str | None = None    # Ngày bắt đầu (None: lấy từ đầu)
    data_end: str | None = None      # Ngày kết thúc (None: lấy đến cuối)
    calib_days: int = 250            # Cửa sổ ước lượng μ, σ (~1 năm)
    horizon: int = 60                # Số phiên dự báo (~3 tháng)
    n_paths: int = 10_000            # Số quỹ đạo mô phỏng (chẵn)
    seed: int = 42                   # Hạt giống ngẫu nhiên
    bt_horizon: int = 20             # Backtest: dự báo trước 20 phiên
    bt_step: int = 10                # Backtest: bước trượt 10 phiên
    bt_paths: int = 2_000            # Backtest: số quỹ đạo mỗi mốc
    out_dir: Path = ROOT / "outputs"
    show_plots: bool = True          # Hiển thị đồng thời 6 figure
