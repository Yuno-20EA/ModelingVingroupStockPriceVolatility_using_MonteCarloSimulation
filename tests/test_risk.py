import numpy as np

from vicmc.analysis.risk import risk_metrics


def test_var_cvar_on_known_terminal_prices():
    # Kiểm tra VaR và CVaR trên phân phối giá xác định (1..100) với S0 = 100
    st = np.arange(1.0, 101.0)
    paths = np.column_stack([np.full(100, 100.0), st])
    m = risk_metrics(paths, 0.0, 0.3)
    ret = st / 100 - 1
    assert np.isclose(m.var95, -np.quantile(ret, 0.05))
    assert np.isclose(m.cvar95, 0.97)              # trung bình của −0.99..−0.95
    assert m.p_profit == 0.0 and m.p_loss_10 == 0.89
