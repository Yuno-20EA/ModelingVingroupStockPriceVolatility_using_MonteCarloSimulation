import numpy as np
from scipy import stats

from vicmc.analysis.risk import risk_metrics
from vicmc.config import DT
from vicmc.model.simulation import simulate_gbm


def test_mean_and_tail_quantiles_match_lognormal_theory():
    """Không dùng trung vị: với biến đối ngẫu nó trùng lý thuyết theo cấu trúc (test vô nghĩa)."""
    mu, sigma, s0, h = 0.2, 0.4, 100.0, 60
    T = h * DT
    m = risk_metrics(simulate_gbm(s0, mu, sigma, h, 200_000, np.random.default_rng(0)), mu, sigma)
    assert abs(m.mean_mc / m.mean_theory - 1) < 0.005
    for level, value in ((0.05, m.q05), (0.95, m.q95)):
        theory = s0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * stats.norm.ppf(level))
        assert abs(value / theory - 1) < 0.005


def test_antithetic_halves_mirror_each_other():
    paths = simulate_gbm(100.0, 0.0, 0.3, 10, 1000, np.random.default_rng(1))
    first, second = np.log(paths[:500, 1:] / 100), np.log(paths[500:, 1:] / 100)
    drift = -0.5 * 0.3**2 * DT * np.arange(1, 11)
    assert np.allclose(first + second, 2 * drift)


def test_odd_path_count_rejected():
    import pytest
    with pytest.raises(ValueError):
        simulate_gbm(100.0, 0.0, 0.3, 5, 3, np.random.default_rng(0))
