import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation
from ._jam_utils import jam_ratios_in_normal_sections

def build_equal(L, vf, vs):
    q = L/6
    return Road([
        Segment("N", q, vf), Segment("S", q, vs),
        Segment("N", q, vf), Segment("S", q, vs),
        Segment("N", q, vf), Segment("S", q, vs),
    ])

def build_unequal(L, vf, vs):
    return Road([
        Segment("N", 0.25*L, vf), Segment("S", 0.25*L, vs),
        Segment("N", 0.15*L, vf), Segment("S", 0.15*L, vs),
        Segment("N", 0.10*L, vf), Segment("S", 0.10*L, vs),
    ])

def _plot(rhos, lj_lists, out, title):
    plt.figure(figsize=(6,4))
    for i, lj in enumerate(lj_lists[:-1]):
        plt.plot(rhos, lj, "o", ms=3, label=f"$l_{{j{i+1}}}$")
    plt.plot(rhos, lj_lists[-1], "^", ms=4, label="sum")
    coef = np.polyfit(rhos, lj_lists[-1], 1)
    th = np.polyval(coef, rhos)
    plt.plot(rhos, th, "-", label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=300)
    plt.close()
    print("[Fig10] Saved:", out)

def run(cfg, device="cpu", vs=1.0,
        rho_min=0.18, rho_max=0.35, rho_steps=18,
        out_a="fig10a_jam_ratio.png", out_b="fig10b_jam_ratio.png"):

    rhos = np.linspace(rho_min, rho_max, int(rho_steps))

    # (a) equal
    lj1, lj2, lj3, ljtot = [], [], [], []
    for rho in rhos:
        L = cfg.N / rho
        road = build_equal(L, cfg.vf_max, vs)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)
        ratios = jam_ratios_in_normal_sections(res["x_mod"].cpu().numpy(),
                                               res["dx"].cpu().numpy(),
                                               road, cfg.dx_threshold)
        while len(ratios) < 3: ratios.append(0.0)
        lj1.append(ratios[0]); lj2.append(ratios[1]); lj3.append(ratios[2])
        ljtot.append(ratios[0]+ratios[1]+ratios[2])
    _plot(rhos, [lj1, lj2, lj3, ljtot], out_a, "Fig10(a)-like: 3 equal slowdowns")

    # (b) unequal
    lj1, lj2, lj3, ljtot = [], [], [], []
    for rho in rhos:
        L = cfg.N / rho
        road = build_unequal(L, cfg.vf_max, vs)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)
        ratios = jam_ratios_in_normal_sections(res["x_mod"].cpu().numpy(),
                                               res["dx"].cpu().numpy(),
                                               road, cfg.dx_threshold)
        while len(ratios) < 3: ratios.append(0.0)
        lj1.append(ratios[0]); lj2.append(ratios[1]); lj3.append(ratios[2])
        ljtot.append(ratios[0]+ratios[1]+ratios[2])
    _plot(rhos, [lj1, lj2, lj3, ljtot], out_b, "Fig10(b)-like: 3 slowdowns unequal")
