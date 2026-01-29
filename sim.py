import torch
import numpy as np
from model_ovm import optimal_velocity_sections

def run_simulation(road, rho, cfg, device="cpu", return_profiles=False):
    """
    Ring road, vehicles indexed in order along ring (no overtaking).
    Keep x unwrapped to avoid periodic cut artifacts.
    Use x_mod = x % L for segment masking.
    """
    torch.manual_seed(cfg.seed)

    dev = torch.device(device)
    dtype = torch.float32

    N = cfg.N
    L = road.length()
    L_t = torch.tensor(L, device=dev, dtype=dtype)

    # initial uniform spacing
    dx0 = L / N
    x = torch.linspace(0.0, L - dx0, N, device=dev, dtype=dtype)  # increasing
    dx_init = torch.full((N,), dx0, device=dev, dtype=dtype)

    # initial velocity = Vopt in each segment
    x_mod = torch.remainder(x, L_t)
    V0 = optimal_velocity_sections(dx_init, x_mod, road, cfg, dev)
    v = V0.clone()

    dt = cfg.dt
    a_sens = torch.tensor(cfg.a_sens, device=dev, dtype=dtype)

    def compute_dx(x_unwrapped):
        dx = torch.empty((N,), device=dev, dtype=dtype)
        dx[:-1] = x_unwrapped[1:] - x_unwrapped[:-1]
        dx[-1]  = (x_unwrapped[0] + L_t) - x_unwrapped[-1]
        return dx

    def f(x_unwrapped, v_vec):
        dx = compute_dx(x_unwrapped)
        x_mod_loc = torch.remainder(x_unwrapped, L_t)
        Vopt = optimal_velocity_sections(dx, x_mod_loc, road, cfg, dev)
        x_dot = v_vec
        v_dot = a_sens * (Vopt - v_vec)
        return x_dot, v_dot, dx, Vopt

    # sampling for current
    samples = []
    for t in range(cfg.t_total):
        # RK4
        k1x, k1v, _, _ = f(x, v)
        k2x, k2v, _, _ = f(x + 0.5*dt*k1x, v + 0.5*dt*k1v)
        k3x, k3v, _, _ = f(x + 0.5*dt*k2x, v + 0.5*dt*k2v)
        k4x, k4v, _, _ = f(x + dt*k3x, v + dt*k3v)

        x = x + (dt/6.0)*(k1x + 2*k2x + 2*k3x + k4x)
        v = v + (dt/6.0)*(k1v + 2*k2v + 2*k3v + k4v)

        # after warmup, sample mean(v)
        if t >= cfg.t_warmup and (t - cfg.t_warmup) % cfg.sample_every == 0:
            samples.append(v.mean().item())

    v_mean = float(np.mean(samples)) if len(samples) else float(v.mean().item())
    current = rho * v_mean

    out = {"current": current, "v_mean": v_mean, "L": L}

    if return_profiles:
        with torch.no_grad():
            dx = compute_dx(x)
            x_mod = torch.remainder(x, L_t)
        out.update({
            "x_mod": x_mod.detach(),
            "x": x.detach(),
            "v": v.detach(),
            "dx": dx.detach(),
        })

    return out
