"""Biểu đồ kiểm định giả thiết GBM."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from ..analysis.diagnostics import Diagnostics
from .common import save_fig


def plot_diagnostics(r: np.ndarray, d: Diagnostics, out: Path) -> None:
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    ax[0].hist(r, bins=60, density=True, alpha=0.7, label="Dữ liệu")
    x = np.linspace(r.min(), r.max(), 400)
    ax[0].plot(x, stats.norm.pdf(x, r.mean(), r.std(ddof=1)), "r", lw=2, label="Chuẩn (giả thiết GBM)")
    ax[0].set_title(f"Phân phối log-return\nđộ nhọn dư = {d.excess_kurt:.2f}, JB p = {d.jb_p:.2g}"); ax[0].legend()
    stats.probplot(r, dist="norm", plot=ax[1])
    ax[1].set_title("Q-Q plot: lệch khỏi đường thẳng = đuôi dày")
    ax[2].bar(np.arange(1, len(d.ac_sq) + 1), d.ac_sq)
    ax[2].axhline(d.ac_band, color="r", ls="--"); ax[2].axhline(-d.ac_band, color="r", ls="--")
    ax[2].set_title(f"ACF của r²  (Ljung-Box p = {d.lb_p:.2g})"); ax[2].set_xlabel("độ trễ (phiên)")
    save_fig(fig, out)
