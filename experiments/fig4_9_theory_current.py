import numpy as np
import matplotlib.pyplot as plt

def theoretical_current(rho, vmax, alpha, x_c):
    dx = 1.0 / rho
    V  = 0.5 * vmax * (np.tanh(alpha*(dx - x_c)) + np.tanh(alpha*x_c))
    return rho * V

def run(cfg,
        rho_min=0.01, rho_max=0.8, rho_steps=300,
        vmax_list=None,
        out="fig4_9_theory_current.png"):

    rhos = np.linspace(rho_min, rho_max, int(rho_steps))
    if vmax_list is None or len(vmax_list) == 0:
        vmax_list = [cfg.vf_max, 1.5, 1.0]

    plt.figure(figsize=(6,4))
    for vmax in vmax_list:
        J = theoretical_current(rhos, vmax, cfg.alpha_ov, cfg.x_f_c)
        plt.plot(rhos, J, label=f"v_max={vmax:g}")

    # bottleneck horizontal line: use smallest vmax as "strongest slowdown"
    bottleneck_v = min(vmax_list)
    Jb = theoretical_current(rhos, bottleneck_v, cfg.alpha_ov, cfg.x_f_c)
    plt.axhline(np.max(Jb), lw=1)

    plt.xlabel("Density $\\rho$")
    plt.ylabel("Current $J$")
    plt.title("Fig4/9-like: Theoretical currents")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=300)
    print("[Fig4/9] Saved:", out)
