"""Điểm vào của chương trình:  python main.py [--tuỳ chọn]"""
from vicmc.cli import parse_args
from vicmc.pipeline import run

if __name__ == "__main__":
    print("\n".join(run(parse_args())))
