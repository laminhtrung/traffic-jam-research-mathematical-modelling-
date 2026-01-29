from dataclasses import dataclass

@dataclass
class SimCfg:
    # --- physics ---
    N: int = 500
    a_sens: float = 2.5          # sensitivity in dv/dt = a(V - v)
    vf_max: float = 2.0          # max speed in normal sections
    alpha_ov: float = 1.0        # slope in tanh of V(dx)
    x_f_c: float = 2.0           # turning point normal
    x_s_c: float = 2.0           # turning point slowdown

    # --- time ---
    dt: float = 1.0 / 128.0
    t_warmup: int = 20000        # steps
    t_total: int = 60000         # steps
    sample_every: int = 20       # steps (sampling for mean current)

    # --- jam detection ---
    dx_threshold: float = 3.0

    # --- misc ---
    seed: int = 0
