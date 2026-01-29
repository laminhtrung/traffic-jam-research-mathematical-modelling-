import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation
from ._jam_utils import jam_ratios_in_normal_sections

def build_road(L, vf, vs):
    q = L/4
    return Road([Segment("N", q, vf), Segment("S", q, vs),
                 Segment("N", q, vf), Segment("S", q, vs)])

def run(cfg, device="cpu", vs=1.0,
        rho_min=0.15, rho_max=0.35, rho_steps=15,
        out="fig5_jam_length_ratio.png"):

    rhos = np.linspace(rho_min, rho_max, int(rho_steps))
    lj1_list, lj2_list, ljtot_list = [], [], []

    for rho in rhos:
        L = cfg.N / rho
        road = build_road(L, cfg.vf_max, vs)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)

        x_mod = res["x_mod"].detach().cpu().numpy()
        dx    = res["dx"].detach().cpu().numpy()

        ratios = jam_ratios_in_normal_sections(x_mod, dx, road, cfg.dx_threshold)
        while len(ratios) < 2: ratios.append(0.0)
        lj1, lj2 = ratios[0], ratios[1]
        lj1_list.append(lj1); lj2_list.append(lj2); ljtot_list.append(lj1+lj2)

    lj1 = np.asarray(lj1_list); lj2 = np.asarray(lj2_list); ljtot = np.asarray(ljtot_list)

    # simple linear fit "theory line"
    coef = np.polyfit(rhos, ljtot, 1)
    th = np.polyval(coef, rhos)

    plt.figure(figsize=(6,4))
    plt.plot(rhos, lj1, "o", label="$l_{j1}$")
    plt.plot(rhos, lj2, "x", label="$l_{j2}$")
    plt.plot(rhos, ljtot, "^", label="$l_{j1}+l_{j2}$")
    plt.plot(rhos, th, "-", label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=300)
    print("[Fig5] Saved:", out)
