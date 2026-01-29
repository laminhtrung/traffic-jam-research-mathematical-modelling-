import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation

def build_road_two(L, vf, vs):
    q = L/4
    return Road([Segment("N", q, vf), Segment("S", q, vs),
                 Segment("N", q, vf), Segment("S", q, vs)])

def _to_np(t):
    return t.detach().cpu().numpy()

def run(cfg, device="cpu", rho=0.25, vs=1.0,
        out_headway="fig3_headway_profile.png",
        out_velocity="fig3_velocity_profile.png"):

    L = cfg.N / rho
    road = build_road_two(L, cfg.vf_max, vs)
    res = run_simulation(road, rho, cfg, device=device, return_profiles=True)

    x = _to_np(res["x"])
    v = _to_np(res["v"])
    dx = _to_np(res["dx"])
    L = float(res["L"])

    # Build continuous spatial axis s from cumulative headway
    cut = int(np.argmin(dx))  # rotate to place shock nicely
    dx_r = np.roll(dx, -cut)
    v_r  = np.roll(v,  -cut)
    s_r  = np.concatenate([[0.0], np.cumsum(dx_r[:-1])])

    marks = [0.0, 0.25*L, 0.50*L, 0.75*L]

    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.step(s_r, dx_r, where="post")
    for m in marks: ax1.axvline(m, lw=1)
    ax1.set_xlabel("Position $s$ (built from cumulative headway)")
    ax1.set_ylabel("Headway $\\Delta x$")
    ax1.set_title(f"Fig3(a)-like: Headway profile ($\\rho={rho}$)")
    ax1.grid(True)
    fig1.tight_layout()
    fig1.savefig(out_headway, dpi=300)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.step(s_r, v_r, where="post")
    for m in marks: ax2.axvline(m, lw=1)
    ax2.set_xlabel("Position $s$ (built from cumulative headway)")
    ax2.set_ylabel("Velocity $v$")
    ax2.set_title(f"Fig3(b)-like: Velocity profile ($\\rho={rho}$)")
    ax2.grid(True)
    fig2.tight_layout()
    fig2.savefig(out_velocity, dpi=300)
    plt.close(fig2)

    print("[Fig3] J =", res["current"])
    return res["current"]
