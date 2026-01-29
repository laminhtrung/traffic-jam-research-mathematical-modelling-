import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from road import Road, Segment
from sim import run_simulation

def build_road_two(L, vf, vs):
    q = L/4
    return Road([Segment("N", q, vf), Segment("S", q, vs),
                 Segment("N", q, vf), Segment("S", q, vs)])

def build_road_one(L, vf, vs):
    q = L/2
    return Road([Segment("N", q, vf), Segment("S", q, vs)])

def theoretical_current(rho, vmax, alpha, x_c):
    dx = 1.0 / rho
    V  = 0.5 * vmax * (np.tanh(alpha*(dx - x_c)) + np.tanh(alpha*x_c))
    return rho * V

def run(cfg, device="cpu", vs=1.0,
        rho_min=0.02, rho_max=0.8, rho_steps=60,
        out="fig2_current_vs_density.png"):

    rhos = np.linspace(rho_min, rho_max, int(rho_steps))
    J_two, J_one = [], []

    for rho in tqdm(rhos, desc="Fig2"):
        L = cfg.N / rho
        road2 = build_road_two(L, cfg.vf_max, vs)
        road1 = build_road_one(L, cfg.vf_max, vs)

        J_two.append(run_simulation(road2, rho, cfg, device=device)["current"])
        J_one.append(run_simulation(road1, rho, cfg, device=device)["current"])

    rhos = np.asarray(rhos)
    J_two = np.asarray(J_two)
    J_one = np.asarray(J_one)

    rho_line = np.linspace(rho_min, rho_max, 400)
    Jf = theoretical_current(rho_line, cfg.vf_max, cfg.alpha_ov, cfg.x_f_c)
    Js = theoretical_current(rho_line, vs,         cfg.alpha_ov, cfg.x_s_c)

    plt.figure(figsize=(6,4))
    plt.plot(rho_line, Jf, "-", lw=1.2, label=f"Vf,max={cfg.vf_max} (theory)")
    plt.plot(rho_line, Js, "-", lw=1.2, label=f"Vs,max={vs} (theory)")
    plt.plot(rhos, J_two, "o", ms=4, label="Two slowdowns (sim)")
    plt.plot(rhos, J_one, "^", ms=4, label="Single slowdown (sim)")
    plt.xlabel("Density $\\rho$")
    plt.ylabel("Current $J$")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=300)
    print("[Fig2] Saved:", out)
