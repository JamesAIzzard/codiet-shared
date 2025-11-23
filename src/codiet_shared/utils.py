from __future__ import annotations
import zlib

def sig_fig_fmt(val: float, sig_figs: int = 4) -> float:
    if val == 0:
        return 0.0
    return float(f"{val:.{sig_figs}g}")


def create_pseudo_uid(value: str) -> int:
    return int(zlib.crc32(value.encode("utf-8")) & 0x7FFFFFFF)
