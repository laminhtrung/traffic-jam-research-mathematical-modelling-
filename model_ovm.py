import torch

def _to_tensor(x, device, dtype):
    if torch.is_tensor(x):
        return x.to(device=device, dtype=dtype)
    return torch.tensor(x, device=device, dtype=dtype)

def V_form(dx, vmax, x_c, alpha_ov):
    """
    V(dx) = 0.5*vmax*(tanh(alpha*(dx-xc)) + tanh(alpha*xc))
    All args must be tensors on same device.
    """
    return 0.5 * vmax * (torch.tanh(alpha_ov * (dx - x_c)) + torch.tanh(alpha_ov * x_c))

def optimal_velocity_sections(dx, x_mod, road, cfg, device):
    """
    dx: (N,) tensor
    x_mod: (N,) tensor in [0, L)
    road: Road with segments
    """
    dtype = dx.dtype
    V = torch.zeros_like(dx)

    alpha = _to_tensor(cfg.alpha_ov, device, dtype)
    xf_c  = _to_tensor(cfg.x_f_c, device, dtype)
    xs_c  = _to_tensor(cfg.x_s_c, device, dtype)

    for (start, end, kind, vmax) in road.bounds:
        start_t = _to_tensor(start, device, dtype)
        end_t   = _to_tensor(end, device, dtype)
        mask = (x_mod >= start_t) & (x_mod < end_t)
        if mask.any():
            vmax_t = _to_tensor(vmax, device, dtype)
            x_c = xf_c if kind == "N" else xs_c
            V[mask] = V_form(dx[mask], vmax_t, x_c, alpha)

    return torch.clamp(V, min=0.0)
