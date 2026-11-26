# Kịch bản độ trôi: đo dự báo nhạy với μ đến mức nào
from dataclasses import dataclass

import numpy as np

from .estimation import GBMParams
from .simulation import simulate_gbm


@dataclass(frozen=True)
class Scenario:
    name: str   # nhãn hiển thị
    slug: str   # dùng đặt tên file
    mu: float


def build_scenarios(params: GBMParams) -> list[Scenario]:
    # μ lịch sử (ngoại suy xu hướng vừa qua) và μ = 0 (không giả định xu hướng)
    return [Scenario("μ lịch sử", "mu_hat", params.mu), Scenario("μ = 0", "mu_zero", 0.0)]


def run_scenarios(s0: float, sigma: float, scenarios: list[Scenario],
                  horizon: int, n_paths: int, seed: int) -> dict[str, np.ndarray]:
    # Cùng hạt giống cho mọi kịch bản (common random numbers): chênh lệch chỉ do μ
    return {sc.slug: simulate_gbm(s0, sc.mu, sigma, horizon, n_paths, np.random.default_rng(seed))
            for sc in scenarios}
