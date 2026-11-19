# Đọc và làm sạch dữ liệu CSV lịch sử giá VIC
import re

import pandas as pd

_COLUMNS = {"ngày": "date", "lần cuối": "close", "mở": "open", "cao": "high", "thấp": "low",
            "kl": "volume", "% thay đổi": "src_pct",
            "date": "date", "time": "date", "close": "close"}
_UNIT = {"": 1.0, "K": 1e3, "M": 1e6, "B": 1e9}


def _number(s: pd.Series) -> pd.Series:
    # Chuyển chuỗi định dạng số có dấu phẩy sang float (ví dụ: '247,800' -> 247800.0)
    return pd.to_numeric(s.str.replace(",", "", regex=False).str.strip(), errors="coerce")


def _volume(s: pd.Series) -> pd.Series:
    # Chuyển khối lượng có ký hiệu K/M/B sang float (ví dụ: '1.21M' -> 1210000.0)
    def one(x: str) -> float:
        m = re.fullmatch(r"\s*([\d.,]+)\s*([KMBkmb]?)\s*", x)
        return float(m.group(1).replace(",", "")) * _UNIT[m.group(2).upper()] if m else float("nan")
    return s.map(one)


def _dates(s: pd.Series) -> pd.DatetimeIndex:
    try:
        return pd.DatetimeIndex(pd.to_datetime(s, format="%d/%m/%Y"))   # Định dạng dd/mm/yyyy
    except ValueError:
        return pd.DatetimeIndex(pd.to_datetime(s))                      # Định dạng ISO yyyy-mm-dd


def load_ohlcv(path) -> pd.DataFrame:
    # Đọc CSV, chuẩn hóa tên cột, chuyển đổi kiểu dữ liệu và sắp xếp tăng dần theo ngày
    raw = pd.read_csv(path, encoding="utf-8-sig", dtype=str)
    raw.columns = [c.strip().lower() for c in raw.columns]
    raw = raw.rename(columns={c: _COLUMNS[c] for c in raw.columns if c in _COLUMNS})
    if not {"date", "close"} <= set(raw.columns):
        raise ValueError(f"Thiếu cột ngày/giá đóng cửa. Cột tìm thấy: {list(raw.columns)}")

    df = pd.DataFrame(index=_dates(raw["date"]))
    df.index.name = "date"
    for col in ("open", "high", "low", "close", "src_pct"):
        if col in raw:
            df[col] = _number(raw[col].str.replace("%", "", regex=False)).values
    if "volume" in raw:
        df["volume"] = _volume(raw["volume"]).values
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")].dropna(subset=["close"])
    return df[df["close"] > 0]


def select_window(df: pd.DataFrame, start: str | None, end: str | None) -> pd.DataFrame:
    # Cắt dữ liệu theo khoảng thời gian [start, end]
    if start:
        df = df[df.index >= pd.Timestamp(start)]
    if end:
        df = df[df.index <= pd.Timestamp(end)]
    return df
