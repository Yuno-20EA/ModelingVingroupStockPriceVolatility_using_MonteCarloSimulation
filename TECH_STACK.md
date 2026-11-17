# Công nghệ & công cụ sử dụng

## Tech stack

| Thành phần | Công nghệ | Dùng để | Module chính |
|---|---|---|---|
| Ngôn ngữ | Python 3.10+ (chạy thử 3.12.3) | Toàn bộ dự án | |
| Tính toán số | NumPy | Sinh số ngẫu nhiên, vector hóa mô phỏng 10.000 quỹ đạo | `model/simulation.py` |
| Xử lý dữ liệu | pandas | Đọc CSV, chuỗi thời gian, cửa sổ trượt | `data/`, `analysis/backtest.py` |
| Thống kê | SciPy | Jarque–Bera, Ljung–Box (χ²), KS, phân phối chuẩn | `analysis/diagnostics.py`, `analysis/backtest.py` |
| Biểu đồ | Matplotlib | 6 hình kết quả | `plots/` |
| Kiểm thử | pytest | 8 test cho lõi tính toán | `tests/` |

Phiên bản đã chạy thử: NumPy 2.5.4, pandas 3.0.6, SciPy 1.18.1, Matplotlib 3.11.2 (yêu cầu tối thiểu ghi trong `requirements.txt`).

## Dữ liệu

- Investing.com: lịch sử giá VIC, 996 phiên, 16/11/2022 → 16/11/2026.

## Công cụ hỗ trợ

| Công cụ | Dùng để |
|---|---|
| Claude,Gemini,Antigrativy,Ollama | Mỗi Agent đều có 1 nhiệm vụ riêng hỗ trợ viết, rà soát và tái cấu trúc code; soạn README. Mọi kết quả đã được chạy lại và đối chiếu |
| Mermaid | Vẽ sơ đồ tư duy và lưu đồ ngay trong README (GitHub tự hiển thị) |
| Markdown | Viết tài liệu |

*(Nhóm : Chủ yếu dùng VS Code, quản lý với Github, công cụ họp nhóm: Discord và gặp nhau trực tiếp trên Giảng Đường.)*
