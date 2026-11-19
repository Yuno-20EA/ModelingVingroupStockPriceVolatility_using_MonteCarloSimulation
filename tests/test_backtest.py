import numpy as np
import pandas as pd

from vicmc.analysis.backtest import rolling_backtest


def test_no_look_ahead():
    # Kiểm tra không nhìn trước tương lai: đổi giá sau mốc i không làm đổi dự báo tại các mốc <= i
    rng = np.random.default_rng(5)
    prices = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.02, 400))), index=pd.bdate_range("2020-01-01", periods=400))
    kw = dict(calib_days=100, horizon=20, step=10, n_paths=500, drift_mode="estimated", seed=1)
    base = rolling_backtest(prices, **kw)
    altered = prices.copy()
    altered.iloc[251:] *= 2
    alt = rolling_backtest(altered, **kw)
    same = [i for i, o in enumerate(base.origin) if prices.index.get_loc(o) <= 250]
    cols = ["q05", "q50", "q95"]
    assert len(same) > 5
    assert np.allclose(base.loc[same, cols], alt.loc[same, cols])
