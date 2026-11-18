import pandas as pd

from vicmc.config import Config
from vicmc.data.loader import _volume, load_ohlcv


def test_real_file_is_parsed():
    df = load_ohlcv(Config().data_path)
    assert len(df) == 996 and df.index.is_monotonic_increasing
    assert df["close"].iloc[0] == 30200 and df["close"].iloc[-1] == 247800
    assert {"open", "high", "low", "close", "volume", "src_pct"} <= set(df.columns)


def test_volume_suffixes():
    assert _volume(pd.Series(["1.21M", "850K", "2.3B", "500"])).tolist() == [1_210_000, 850_000, 2.3e9, 500]
