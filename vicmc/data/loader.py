"""Đọc & làm sạch CSV giá (định dạng Investing.com tiếng Việt)."""
import re

import pandas as pd

_COLUMNS = {"ngày": "date", "lần cuối": "close", "mở": "open", "cao": "high", "thấp": "low",
            "kl": "volume", "% thay đổi": "src_pct",
            "date": "date", "time": "date", "close": "close"}   # CSV tối giản (date, close)
_UNIT = {"": 1.0, "K": 1e3, "M": 1e6, "B": 1e9}


def _number(s: pd.Series) -> pd.Series:
    """'247,800' -> 247800.0 (dấu phẩy là phân cách hàng nghìn)."""
    return pd.to_numeric(s.str.replace(",", "", regex=False).str.strip(), errors="coerce")


def _volume(s: pd.Series) -> pd.Series:
    """'1.21M' -> 1_210_000."""
    def one(x: str) -> float:
        m = re.fullmatch(r"\s*([\d.,]+)\s*([KMBkmb]?)\s*", x)
        return float(m.group(1).replace(",", "")) * _UNIT[m.group(2).upper()] if m else float("nan")
    return s.map(one)


def _dates(s: pd.Series) -> pd.DatetimeIndex:
    try:
        return pd.DatetimeIndex(pd.to_datetime(s, format="%d/%m/%Y"))   # dd/mm/yyyy
    except ValueError:
        return pd.DatetimeIndex(pd.to_datetime(s))                      # ISO


def load_ohlcv(path) -> pd.DataFrame:
    """CSV -> DataFrame tăng dần theo ngày; cột: open, high, low, close, volume, src_pct."""
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
    """Cắt theo khoảng [start, end] (None = không giới hạn)."""
    if start:
        df = df[df.index >= pd.Timestamp(start)]
    if end:
        df = df[df.index <= pd.Timestamp(end)]
    return df
