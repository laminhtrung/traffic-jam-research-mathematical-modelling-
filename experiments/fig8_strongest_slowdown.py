import numpy as np
import matplotlib.pyplot as plt
from road import Road, Segment
from sim import run_simulation
from ._jam_utils import jam_ratios_in_normal_sections

def build_road(L, vf, vs1, vs2):
    q = L/4
    return Road([Segment("N", q, vf), Segment("S", q, vs1),
                 Segment("N", q, vf), Segment("S", q, vs2)])

def run(cfg, device="cpu", vs1=1.5, vs2=1.0,
        out_prefix="fig8"):

    # headway profiles at 3 rhos
    for rho in [0.16, 0.25, 0.33]:
        L = cfg.N / rho
        road = build_road(L, cfg.vf_max, vs1, vs2)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)

        x = res["x_mod"].detach().cpu().numpy()
        dx = res["dx"].detach().cpu().numpy()
        order = np.argsort(x)
        x = x[order]; dx = dx[order]

        plt.figure(figsize=(6,4))
        plt.step(x, dx, where="post")
        plt.xlabel("Position")
        plt.ylabel("Headway")
        plt.title(f"Fig8-like headway ($\\rho={rho}$, vs1={vs1}, vs2={vs2})")
        plt.grid(True)
        plt.tight_layout()
        out = f"{out_prefix}_headway_rho{int(rho*100):02d}.png"
        plt.savefig(out, dpi=300)
        plt.close()
        print("[Fig8] Saved:", out)

    # jam length ratio vs density
    rhos = np.linspace(0.15, 0.40, 16)
    lj1_list, lj2_list, ljtot_list = [], [], []
    for rho in rhos:
        L = cfg.N / rho
        road = build_road(L, cfg.vf_max, vs1, vs2)
        res = run_simulation(road, rho, cfg, device=device, return_profiles=True)

        x_mod = res["x_mod"].detach().cpu().numpy()
        dx    = res["dx"].detach().cpu().numpy()
        ratios = jam_ratios_in_normal_sections(x_mod, dx, road, cfg.dx_threshold)
        while len(ratios) < 2: ratios.append(0.0)
        lj1, lj2 = ratios[0], ratios[1]
        lj1_list.append(lj1); lj2_list.append(lj2); ljtot_list.append(lj1+lj2)

    ljtot = np.asarray(ljtot_list)
    coef = np.polyfit(rhos, ljtot, 1)
    th = np.polyval(coef, rhos)

    plt.figure(figsize=(6,4))
    plt.plot(rhos, lj1_list, "o", label="$l_{j1}$")
    plt.plot(rhos, lj2_list, "x", label="$l_{j2}$")
    plt.plot(rhos, ljtot_list, "^", label="$l_{j1}+l_{j2}$")
    plt.plot(rhos, th, "-", label="theory (fit)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Jam length ratio")
    plt.title("Fig8(d)-like jam length ratio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    out = f"{out_prefix}_jam_ratio.png"
    plt.savefig(out, dpi=300)
    plt.close()
    print("[Fig8] Saved:", out)
