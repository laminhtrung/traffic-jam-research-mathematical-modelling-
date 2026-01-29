import numpy as np

def jam_ratios_in_normal_sections(x_mod, dx, road, dx_threshold):
    """
    Return jam-length ratio for each normal segment (N1, N2, ...).
    Jam definition: dx < dx_threshold.
    """
    L = road.length()
    x = np.asarray(x_mod)
    dx = np.asarray(dx)

    # Sort by x for per-segment masking
    order = np.argsort(x)
    xs = x[order]
    dxs = dx[order]

    ratios = []
    for (start, end, kind, vmax) in road.bounds:
        if kind != "N":
            continue
        mask = (xs >= start) & (xs < end)
        if not np.any(mask):
            ratios.append(0.0); continue
        xs_sec = xs[mask]
        dx_sec = dxs[mask]
        jam_mask = dx_sec < dx_threshold
        if not np.any(jam_mask):
            ratios.append(0.0); continue
        jam_x = xs_sec[jam_mask]
        length = jam_x.max() - jam_x.min()
        ratios.append(length / L)
    return ratios
