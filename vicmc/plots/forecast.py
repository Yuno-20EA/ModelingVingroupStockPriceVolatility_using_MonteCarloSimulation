# Biểu đồ dự báo: fan chart và phân phối giá cuối kỳ
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..analysis.risk import quantile_paths
from .common import save_fig, vnd_axis


def plot_fan(prices: pd.Series, paths: np.ndarray, future_idx: pd.DatetimeIndex,
             label: str, hist_days: int, out: Path) -> None:
    # Vẽ lịch sử giá, 30 quỹ đạo mẫu và các dải phân vị 50% / 90%
    qs = quantile_paths(paths)
    idx = pd.DatetimeIndex([prices.index[-1]]).append(future_idx)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(prices.index[-hist_days:], prices.values[-hist_days:], color="black", lw=1.5, label="Lịch sử")
    for k in range(30):
        ax.plot(idx, paths[k], lw=0.5, alpha=0.35)
    ax.fill_between(idx, qs[0], qs[4], color="tab:blue", alpha=0.18, label="Khoảng 90% (5%-95%)")
    ax.fill_between(idx, qs[1], qs[3], color="tab:blue", alpha=0.30, label="Khoảng 50% (25%-75%)")
    ax.plot(idx, qs[2], color="tab:blue", lw=2, label="Trung vị dự báo")
    ax.plot(idx, paths.mean(axis=0), color="tab:green", ls="--", lw=1.5, label="Kỳ vọng E[S_t]")
    ax.set_title(f"Fan chart dự báo Monte Carlo giá VIC, kịch bản {label}")
    ax.set_ylabel("Giá (VND)"); vnd_axis(ax); ax.legend(loc="upper left"); ax.grid(alpha=0.3)
    save_fig(fig, out)


def plot_terminal_compare(paths_by_label: dict[str, np.ndarray], horizon: int, out: Path) -> None:
    # So sánh phân phối giá cuối kỳ giữa các kịch bản (đường đứt: trung vị)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for (label, paths), color in zip(paths_by_label.items(), ["tab:blue", "tab:orange", "tab:green"]):
        ax.hist(paths[:, -1], bins=80, density=True, histtype="step", lw=2, color=color, label=label)
        ax.axvline(np.median(paths[:, -1]), color=color, ls="--", lw=1)
    s0 = next(iter(paths_by_label.values()))[0, 0]
    ax.axvline(s0, color="black", label=f"Giá hiện tại S0 = {s0:,.0f}")
    ax.set_title(f"Phân phối giá VIC sau {horizon} phiên theo kịch bản")
    ax.set_xlabel("Giá (VND)"); vnd_axis(ax, "x"); ax.legend(); ax.grid(alpha=0.3)
    save_fig(fig, out)
