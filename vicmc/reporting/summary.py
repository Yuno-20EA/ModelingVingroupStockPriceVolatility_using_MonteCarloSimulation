"""Dựng báo cáo văn bản summary.txt (chỉ định dạng, không tính toán)."""
from ..analysis.backtest import BacktestSummary
from ..analysis.diagnostics import Diagnostics
from ..analysis.risk import RiskMetrics
from ..config import Config
from ..data.quality import DataQuality
from ..model.estimation import GBMParams
from ..model.scenarios import Scenario


def quality_lines(q: DataQuality) -> list[str]:
    lines = ["=== 1. CHẤT LƯỢNG DỮ LIỆU ===",
             f"Số phiên: {q.n_obs} ({q.start.date()} -> {q.end.date()})",
             f"Giá đóng cửa: min = {q.min_close:,.0f}, max = {q.max_close:,.0f}, toàn kỳ tăng {q.total_growth_x:.2f} lần",
             f"Khoảng trống > 4 ngày: {q.n_long_gaps} lần (lớn nhất {q.max_gap_days} ngày; thường là nghỉ lễ/Tết)",
             f"|log-return| lớn nhất: {q.max_abs_logret:.2%} | số phiên sát biên ±7%: {q.n_near_limit}"]
    if q.n_src_mismatch is not None:
        verdict = "giá liên tục, không thấy dấu hiệu chưa điều chỉnh" if q.n_src_mismatch == 0 else "CẦN KIỂM TRA điều chỉnh cổ tức/chia tách"
        lines.append(f"Phiên lệch giữa '% thay đổi' của nguồn và giá tự tính: {q.n_src_mismatch} ({verdict})")
    return lines + [""]


def params_lines(p: GBMParams, d: Diagnostics) -> list[str]:
    return ["=== 2. ƯỚC LƯỢNG THAM SỐ GBM ===",
            f"Cửa sổ hiệu chỉnh: {p.start.date()} -> {p.end.date()} ({p.n_returns} log-return)",
            f"μ̂ = {p.mu:.4f}/năm (sai số chuẩn ±{p.se_mu:.3f}) | σ̂ = {p.sigma:.4f}/năm", "",
            "=== 3. KIỂM ĐỊNH GIẢ THIẾT ===",
            f"Độ lệch = {d.skew:.3f} | độ nhọn dư = {d.excess_kurt:.3f} | Jarque-Bera p = {d.jb_p:.3g}",
            f"Ljung-Box trên r² (20 độ trễ): Q = {d.lb_stat:.1f}, p = {d.lb_p:.3g}", ""]


def forecast_lines(cfg: Config, s0: float, rows: list[tuple[Scenario, RiskMetrics]]) -> list[str]:
    lines = [f"=== 4. DỰ BÁO {cfg.horizon} PHIÊN TỚI (S0 = {s0:,.0f} VND, {cfg.n_paths} quỹ đạo) ==="]
    for sc, m in rows:
        lines += [f"[Kịch bản {sc.name}]  μ = {sc.mu:.4f}/năm",
                  f"  E[S_T]     MC = {m.mean_mc:,.0f} | lý thuyết = {m.mean_theory:,.0f}",
                  f"  Trung vị   MC = {m.median_mc:,.0f} | lý thuyết = {m.median_theory:,.0f}"
                  "  (trùng theo cấu trúc do biến đối ngẫu, không phải bằng chứng kiểm chứng)",
                  f"  Khoảng 90%: [{m.q05:,.0f}, {m.q95:,.0f}]",
                  f"  VaR95 = {m.var95:.2%} | CVaR95 = {m.cvar95:.2%}",
                  f"  P(lãi) = {m.p_profit:.1%} | P(lỗ>10%) = {m.p_loss_10:.1%} | P(lãi>20%) = {m.p_gain_20:.1%}"]
    return lines + [""]


def backtest_lines(cfg: Config, results: dict[str, BacktestSummary]) -> list[str]:
    lines = [f"=== 5. BACKTEST CUỐN CHIẾU (dự báo trước {cfg.bt_horizon} phiên, hiệu chỉnh {cfg.calib_days} phiên) ==="]
    for name, s in results.items():
        lines += [f"[Backtest, kịch bản {name}] {s.n_origins} mốc",
                  f"  Độ phủ 90%: {s.coverage_90:.1%} (lý tưởng 90%) | độ phủ 50%: {s.coverage_50:.1%} (lý tưởng 50%)",
                  f"  Giá thực dưới dải 90%: {s.below_q05:.1%} (lý tưởng 5%) | trên dải 90%: {s.above_q95:.1%} (lý tưởng 5%)",
                  f"  MAPE của trung vị: {s.mape_median:.2%}",
                  f"  KS test PIT~U(0,1): thống kê = {s.ks_stat:.3f}, p = {s.ks_p:.3g} "
                  "(các mốc chồng lấn nên p-value chỉ mang tính tham khảo)"]
    return lines
