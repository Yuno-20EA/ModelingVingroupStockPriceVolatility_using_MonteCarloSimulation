"""Điểm vào của chương trình:  python main.py [--tuỳ chọn]"""
import io
import sys

from vicmc.cli import parse_args
from vicmc.pipeline import run

if __name__ == "__main__":
    if isinstance(sys.stdout, io.TextIOWrapper):   # in được tiếng Việt trên mọi console
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(run(parse_args())))
