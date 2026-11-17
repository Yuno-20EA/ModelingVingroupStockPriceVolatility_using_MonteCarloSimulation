import numpy as np
import pandas as pd

from vicmc.config import TRADING_DAYS
from vicmc.model.estimation import estimate_gbm
from vicmc.model.simulation import simulate_gbm


def test_recovers_sigma_and_mu_within_error():
    mu, sigma = 0.1, 0.35
    path = simulate_gbm(100.0, mu, sigma, TRADING_DAYS * 40, 2, np.random.default_rng(2))[0]
    p = estimate_gbm(pd.Series(path, index=pd.bdate_range("1990-01-01", periods=len(path))))
    assert abs(p.sigma - sigma) < 0.01
    assert abs(p.mu - mu) < 3 * p.se_mu
