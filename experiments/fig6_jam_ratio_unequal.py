import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation
from ._jam_utils import jam_ratios_in_normal_sections

def build_road(L, vf, vs):
    """
    Fig6-like geometry:
      LN1=0.35L, LS1=0.25L, LN2=0.15L, LS2=0.25L  (sum=1.0L)
    """
    return Road([
        Segment("N", 0.35 * L, vf),
        Segment("S", 0.25 * L, vs),
        Segment("N", 0.15 * L, vf),
        Segment("S", 0.25 * L, vs),
    ])

def run(cfg, device="cpu", vs=1.0,
        rho=0.31,
        rho_min=0.15, rho_max=0.35, rho_steps=15,
        out_profile="fig6a_headway_profile.png",
        out_ratio="fig6b_jam_length_ratio.png"):

    # -------------------------
    # (a) Headway profile at rho_profile
    # -------------------------
    rho = float(rho)
    L = cfg.N / rho
    road = build_road(L, cfg.vf_max, vs)

    res = run_simulation(road, rho, cfg, device=device, return_profiles=True)
    x = res["x_mod"].detach().cpu().numpy()
    dx = res["dx"].detach().cpu().numpy()

    order = np.argsort(x)
    x = x[order]
    dx = dx[order]

    plt.figure(figsize=(6, 4))
    plt.step(x, dx, where="post")
    # draw segment boundaries
    pos = 0.0
    for (start, end, kind, vmax) in road.bounds:
        plt.axvline(pos, lw=1)
        pos = end
    plt.axvline(road.length(), lw=1)

    plt.xlabel("Position")
    plt.ylabel("Headway $\\Delta x$")
    plt.title(f"Fig6(a)-like: Headway profile ($\\rho={rho}$)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_profile, dpi=300)
    plt.close()
    print("[Fig6a] Saved:", out_profile)

    # -------------------------
    # (b) Jam-length ratio vs density
    # -------------------------
    rhos = np.linspace(rho_min, rho_max, int(rho_steps))
    lj1_list, lj2_list, ljtot_list = [], [], []

    for rho in rhos:
        L = cfg.N / rho
        road = build_road(L, cfg.vf_max, vs)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)

        ratios = jam_ratios_in_normal_sections(
            res["x_mod"].detach().cpu().numpy(),
            res["dx"].detach().cpu().numpy(),
            road,
            cfg.dx_threshold
        )
        while len(ratios) < 2:
            ratios.append(0.0)

        lj1, lj2 = ratios[0], ratios[1]
        lj1_list.append(lj1)
        lj2_list.append(lj2)
        ljtot_list.append(lj1 + lj2)

    # simple linear fit as "theory line" (same style as your Fig5)
    coef = np.polyfit(rhos, ljtot_list, 1)
    th = np.polyval(coef, rhos)

    plt.figure(figsize=(6, 4))
    plt.plot(rhos, lj1_list, "o", ms=4, label="$l_{j1}$ (N1)")
    plt.plot(rhos, lj2_list, "x", ms=4, label="$l_{j2}$ (N2)")
    plt.plot(rhos, ljtot_list, "^", ms=4, label="$l_{j1}+l_{j2}$")
    plt.plot(rhos, th, "-", lw=1.2, label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.title("Fig6(b)-like: Jam-length ratio vs density")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_ratio, dpi=300)
    plt.close()
    print("[Fig6b] Saved:", out_ratio)
