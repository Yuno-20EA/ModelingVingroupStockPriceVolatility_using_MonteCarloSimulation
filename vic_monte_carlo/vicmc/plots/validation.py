"""Biểu đồ kết quả backtest."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .common import save_fig, vnd_axis


def plot_backtest(bt_by_label: dict[str, pd.DataFrame], horizon: int, out: Path) -> None:
    """Hàng trên: giá thực vs dải 90%. Hàng dưới: histogram PIT (đều = hiệu chuẩn tốt, chữ U = đánh giá thấp rủi ro)."""
    fig, ax = plt.subplots(2, len(bt_by_label), figsize=(7 * len(bt_by_label), 9), squeeze=False)
    for j, (label, bt) in enumerate(bt_by_label.items()):
        top, bottom = ax[0, j], ax[1, j]
        top.fill_between(bt.target, bt.q05, bt.q95, alpha=0.25, label="Dải dự báo 90%")
        top.plot(bt.target, bt.q50, lw=1, label="Trung vị dự báo")
        top.scatter(bt.target, bt.actual, s=12, color="red", label="Giá thực tế", zorder=3)
        top.set_title(f"Backtest {horizon} phiên, kịch bản {label}")
        top.set_ylabel("Giá (VND)"); vnd_axis(top); top.legend(); top.grid(alpha=0.3)
        bottom.hist(bt.pit, bins=10, range=(0, 1), density=True, alpha=0.7)
        bottom.axhline(1.0, color="r", ls="--", label="Lý tưởng: Uniform(0,1)")
        bottom.set_title(f"Histogram PIT, kịch bản {label}"); bottom.set_xlabel("PIT"); bottom.legend()
    save_fig(fig, out)
