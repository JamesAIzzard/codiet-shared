def sig_fig_fmt(val: float, sig_figs: int = 4) -> float:
    if val == 0:
        return 0.0
    return float(f"{val:.{sig_figs}g}")