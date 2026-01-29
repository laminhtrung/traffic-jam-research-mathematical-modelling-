# traffic_jam_paper/metrics.py
import numpy as np
from typing import Dict, Tuple

# Allow running both as a package and as a plain script workspace.
try:
    from .road import Road
except ImportError:  # pragma: no cover
    from road import Road

def jam_length_by_section(profile: Dict, road: Road, jam_headway_threshold: float) -> Dict[str, float]:
    """
    Estimate jam length in each Normal section N_k as in paper Fig5-7: jam is in normal section before slowdown.
    We approximate jam region by positions where headway < threshold (dense) AND vehicle is in Normal section.
    Then jam length ≈ sum of local headways (dx) for jam vehicles.

    Returns:
      {"N1": lJ1/L, "N2": lJ2/L, ... , "total": sum/L}
    """
    x = profile["x"]
    dx = profile["dx"]
    kind = profile["kind"]   # 0=N,1=S
    L = road.L

    # assign section index counting only N sections in order along road
    # We map each vehicle to which N segment it lies in.
    labels = road.labels()
    # build cumulative boundaries and N indices
    N_spans = []
    nidx = 0
    for seg_kind, a, b in labels:
        if seg_kind == "N":
            nidx += 1
            N_spans.append((nidx, a, b))

    # vehicle -> N_k (or 0 if not in normal)
    Nk = np.zeros_like(x, dtype=int)
    xm = np.mod(x, L)
    for k, a, b in N_spans:
        mask = (xm >= a) & (xm < b)
        Nk[mask] = k

    jam_mask = (kind == 0) & (dx < jam_headway_threshold) & (Nk > 0)

    out = {}
    total = 0.0
    for k, _, _ in N_spans:
        Lk = float(np.sum(dx[jam_mask & (Nk == k)]))
        out[f"N{k}"] = Lk / L
        total += Lk
    out["total"] = total / L
    return out
