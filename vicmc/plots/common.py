# Tiện ích trực quan hóa và hiển thị biểu đồ dùng chung
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def vnd_axis(ax, axis: str = "y") -> None:
    # Định dạng trục giá trị tiền tệ có dấu phân cách hàng nghìn (ví dụ: 247,800 VND)
    fmt = FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def save_fig(fig, path: Path) -> None:
    # Căn chỉnh, lưu biểu đồ ra file và gán tiêu đề cho cửa sổ hiển thị
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300)
    if getattr(fig.canvas, "manager", None):
        fig.canvas.manager.set_window_title(path.stem)


def show_plots() -> None:
    # Hiển thị đồng thời toàn bộ 6 figure đã vẽ lên màn hình
    plt.show()
    plt.close("all")
