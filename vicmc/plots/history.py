"""Biểu đồ dữ liệu lịch sử và tham số trượt."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .common import save_fig, vnd_axis


def plot_history(prices: pd.Series, calib_start: pd.Timestamp, out: Path) -> None:
    r = np.log(prices).diff()
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    ax[0].semilogy(prices.index, prices.values, lw=1.2)   # thang log: hợp với quá trình nhân tính
    ax[0].axvspan(calib_start, prices.index[-1], color="orange", alpha=0.15, label="Cửa sổ hiệu chỉnh")
    ax[0].set_title("Giá đóng cửa VIC (thang log) và cửa sổ ước lượng tham số")
    ax[0].set_ylabel("Giá đóng cửa (VND)"); vnd_axis(ax[0]); ax[0].legend(); ax[0].grid(alpha=0.3, which="both")
    ax[1].plot(r.index, r.values, lw=0.6, color="tab:red")
    ax[1].set_title("Log-return ngày  r_t = ln(S_t / S_{t-1})"); ax[1].grid(alpha=0.3)
    save_fig(fig, out)


def plot_rolling_params(roll: pd.DataFrame, window: int, out: Path) -> None:
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    for a, col, color, title in ((ax[0], "mu", "tab:green", "Độ trôi μ̂"), (ax[1], "sigma", "tab:purple", "Độ biến động σ̂")):
        a.plot(roll.index, roll[col] * 100, color=color)
        a.set_title(f"{title} trên cửa sổ trượt {window} phiên (%/năm)"); a.grid(alpha=0.3)
    ax[0].axhline(0, color="black", lw=0.8)
    save_fig(fig, out)
