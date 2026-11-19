# Điều phối luồng xử lý: nạp dữ liệu -> ước lượng -> mô phỏng -> backtest -> báo cáo
from . import plots
from .analysis.backtest import rolling_backtest, summarize_backtest
from .analysis.diagnostics import run_diagnostics
from .analysis.risk import risk_metrics
from .config import Config
from .data.loader import load_ohlcv, select_window
from .data.quality import check_quality
from .data.returns import log_returns
from .model.estimation import estimate_gbm, rolling_estimates
from .model.scenarios import build_scenarios, run_scenarios
from .model.simulation import future_dates
from .reporting import summary, tables

BACKTEST_MODES = {"μ ước lượng": "estimated", "μ = 0": "zero"}


def run(cfg: Config) -> list[str]:
    fig_dir, tab_dir = cfg.out_dir / "figures", cfg.out_dir / "tables"
    tab_dir.mkdir(parents=True, exist_ok=True)

    # 1. Dữ liệu
    df = select_window(load_ohlcv(cfg.data_path), cfg.data_start, cfg.data_end)
    prices = df["close"]
    if len(prices) < cfg.calib_days + cfg.bt_horizon + 10:
        raise SystemExit(f"Dữ liệu quá ngắn ({len(prices)} phiên) so với calib_days = {cfg.calib_days}.")

    # 2-3. Ước lượng và kiểm định trên cửa sổ hiệu chỉnh
    calib = prices.iloc[-(cfg.calib_days + 1):]
    params, r = estimate_gbm(calib), log_returns(calib)
    diag = run_diagnostics(r)

    # 4-5. Monte Carlo theo kịch bản và rủi ro
    s0 = float(prices.iloc[-1])
    scenarios = build_scenarios(params)
    paths = run_scenarios(s0, params.sigma, scenarios, cfg.horizon, cfg.n_paths, cfg.seed)
    risks = [(sc, risk_metrics(paths[sc.slug], sc.mu, params.sigma)) for sc in scenarios]
    dates = future_dates(prices.index[-1], cfg.horizon)

    # 6. Backtest cuốn chiếu
    bt = {label: rolling_backtest(prices, cfg.calib_days, cfg.bt_horizon, cfg.bt_step,
                                  cfg.bt_paths, mode, cfg.seed + 1)
          for label, mode in BACKTEST_MODES.items()}

    # 7. Biểu đồ, bảng, báo cáo
    main_sc = scenarios[0]
    plots.plot_history(prices, calib.index[0], fig_dir / "fig1_history.png")
    plots.plot_rolling_params(rolling_estimates(prices, cfg.calib_days), cfg.calib_days, fig_dir / "fig2_rolling_params.png")
    plots.plot_diagnostics(r, diag, fig_dir / "fig3_diagnostics.png")
    plots.plot_fan(prices, paths[main_sc.slug], dates, main_sc.name, 120, fig_dir / "fig4_fan_chart.png")
    plots.plot_terminal_compare({sc.name: paths[sc.slug] for sc in scenarios}, cfg.horizon, fig_dir / "fig5_terminal_scenarios.png")
    plots.plot_backtest(bt, cfg.bt_horizon, fig_dir / "fig6_backtest.png")

    for sc in scenarios:
        tables.save_forecast(paths[sc.slug], prices.index[-1:].append(dates), tab_dir / f"forecast_{sc.slug}.csv")
    for label, mode in BACKTEST_MODES.items():
        tables.save_backtest(bt[label], tab_dir / f"backtest_{mode}.csv")

    lines = (summary.quality_lines(check_quality(df)) + summary.params_lines(params, diag)
             + summary.forecast_lines(cfg, s0, risks)
             + summary.backtest_lines(cfg, {k: summarize_backtest(v) for k, v in bt.items()}))
    summary_text = "\n".join(lines)
    (cfg.out_dir / "summary.txt").write_text(summary_text, encoding="utf-8")
    print("\n" + summary_text + "\n")

    if cfg.show_plots:
        plots.show_plots()

    return lines
