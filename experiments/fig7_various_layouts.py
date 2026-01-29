import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation
from ._jam_utils import jam_ratios_in_normal_sections

def build_road_a(L, vf, vs):
    """
    Fig7(a)-like:
      LN1=LN2=0.25L
      LS1=0.35L, LS2=0.15L
    """
    return Road([
        Segment("N", 0.25 * L, vf),
        Segment("S", 0.35 * L, vs),
        Segment("N", 0.25 * L, vf),
        Segment("S", 0.15 * L, vs),
    ])

def build_road_b(L, vf, vs):
    """
    Fig7(b)-like (example alternate layout):
      LN1=0.15L, LS1=0.15L, LN2=0.35L, LS2=0.35L
    """
    return Road([
        Segment("N", 0.15 * L, vf),
        Segment("S", 0.15 * L, vs),
        Segment("N", 0.35 * L, vf),
        Segment("S", 0.35 * L, vs),
    ])

def _run_ratio_curve(cfg, device, vs, build_fn, rho_min, rho_max, rho_steps):
    rhos = np.linspace(rho_min, rho_max, int(rho_steps))
    lj1_list, lj2_list, ljtot_list = [], [], []

    for rho in rhos:
        L = cfg.N / rho
        road = build_fn(L, cfg.vf_max, vs)
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

    # linear fit theory line
    coef = np.polyfit(rhos, ljtot_list, 1)
    th = np.polyval(coef, rhos)
    return rhos, lj1_list, lj2_list, ljtot_list, th

def run(cfg, device="cpu", vs=1.0,
        rho_min=0.15, rho_max=0.35, rho_steps=15,
        out_a="fig7a_jam_length_ratio.png",
        out_b="fig7b_jam_length_ratio.png"):

    # -------- Fig7(a) ----------
    rhos, lj1, lj2, ljtot, th = _run_ratio_curve(
        cfg, device, vs, build_road_a, rho_min, rho_max, rho_steps
    )

    plt.figure(figsize=(6, 4))
    plt.plot(rhos, lj1, "o", ms=4, label="$l_{j1}$ (N1)")
    plt.plot(rhos, lj2, "x", ms=4, label="$l_{j2}$ (N2)")
    plt.plot(rhos, ljtot, "^", ms=4, label="$l_{j1}+l_{j2}$")
    plt.plot(rhos, th, "-", lw=1.2, label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.title("Fig7(a)-like: Jam-length ratio vs density")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_a, dpi=300)
    plt.close()
    print("[Fig7a] Saved:", out_a)

    # -------- Fig7(b) ----------
    rhos, lj1, lj2, ljtot, th = _run_ratio_curve(
        cfg, device, vs, build_road_b, rho_min, rho_max, rho_steps
    )

    plt.figure(figsize=(6, 4))
    plt.plot(rhos, lj1, "o", ms=4, label="$l_{j1}$ (N1)")
    plt.plot(rhos, lj2, "x", ms=4, label="$l_{j2}$ (N2)")
    plt.plot(rhos, ljtot, "^", ms=4, label="$l_{j1}+l_{j2}$")
    plt.plot(rhos, th, "-", lw=1.2, label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.title("Fig7(b)-like: Jam-length ratio vs density")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_b, dpi=300)
    plt.close()
    print("[Fig7b] Saved:", out_b)
