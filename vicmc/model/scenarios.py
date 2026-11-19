# Thiết lập các kịch bản độ trôi (drift scenarios) để so sánh
from dataclasses import dataclass

import numpy as np

from .estimation import GBMParams
from .simulation import simulate_gbm


@dataclass(frozen=True)
class Scenario:
    name: str   # Tên hiển thị
    slug: str   # Tên định danh file
    mu: float


def build_scenarios(params: GBMParams) -> list[Scenario]:
    # Kịch bản 1: μ lịch sử (ước lượng từ mẫu); Kịch bản 2: μ = 0 (trung lập rủi ro)
    return [Scenario("μ lịch sử", "mu_hat", params.mu), Scenario("μ = 0", "mu_zero", 0.0)]


def run_scenarios(s0: float, sigma: float, scenarios: list[Scenario],
                  horizon: int, n_paths: int, seed: int) -> dict[str, np.ndarray]:
    # Chạy mô phỏng dùng chung số ngẫu nhiên (CRN) để loại trừ sai số mẫu khi so sánh
    return {sc.slug: simulate_gbm(s0, sc.mu, sigma, horizon, n_paths, np.random.default_rng(seed))
            for sc in scenarios}
