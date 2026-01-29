import argparse
from config import SimCfg

from experiments.fig2_fundamental import run as run_fig2
from experiments.fig3_profile import run as run_fig3
from experiments.fig4_9_theory_current import run as run_fig4_9
from experiments.fig5_jam_ratio_equal import run as run_fig5
from experiments.fig8_strongest_slowdown import run as run_fig8
from experiments.fig10_three_slowdowns import run as run_fig10
from experiments.fig6_jam_ratio_unequal import run as run_fig6
from experiments.fig7_various_layouts import run as run_fig7


FIG_RUNNERS = {
    "2": run_fig2,
    "3": run_fig3,
    "4": run_fig4_9,
    "9": run_fig4_9,
    "5": run_fig5,
    "6": run_fig6,
    "7": run_fig7,
    "8": run_fig8,
    "10": run_fig10,
}

def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--fig", nargs="+", required=True)

    p.add_argument("--device", type=str, default="cpu")

    # overrides cfg
    p.add_argument("--N", type=int, default=None)
    p.add_argument("--a_sens", type=float, default=None)
    p.add_argument("--vf_max", type=float, default=None)
    p.add_argument("--alpha_ov", type=float, default=None)
    p.add_argument("--x_f_c", type=float, default=None)
    p.add_argument("--x_s_c", type=float, default=None)
    p.add_argument("--dt", type=float, default=None)
    p.add_argument("--t_warmup", type=int, default=None)
    p.add_argument("--t_total", type=int, default=None)
    p.add_argument("--sample_every", type=int, default=None)
    p.add_argument("--dx_threshold", type=float, default=None)

    # common params
    p.add_argument("--rho", type=float, default=0.25)
    p.add_argument("--vs", type=float, default=1.0)
    p.add_argument("--vs1", type=float, default=1.5)
    p.add_argument("--vs2", type=float, default=1.0)

    # sweep for fig2/fig4/9
    p.add_argument("--rho_min", type=float, default=0.02)
    p.add_argument("--rho_max", type=float, default=0.80)
    p.add_argument("--rho_steps", type=int, default=60)
    p.add_argument("--vmax_list", nargs="+", type=float, default=None)

    # outputs
    p.add_argument("--out", type=str, default="out.png")
    p.add_argument("--out_headway", type=str, default="fig3_headway.png")
    p.add_argument("--out_velocity", type=str, default="fig3_velocity.png")
    p.add_argument("--out_prefix", type=str, default="fig8")
    p.add_argument("--out_a", type=str, default="fig10a.png")
    p.add_argument("--out_b", type=str, default="fig10b.png")
    p.add_argument("--out_profile", type=str, default="profile.png")
    p.add_argument("--out_ratio", type=str, default="ratio.png")

    return p

def apply_overrides(cfg, args):
    for k in ["N","a_sens","vf_max","alpha_ov","x_f_c","x_s_c","dt",
              "t_warmup","t_total","sample_every","dx_threshold"]:
        v = getattr(args, k, None)
        if v is not None:
            setattr(cfg, k, v)

def main():
    args = build_parser().parse_args()
    cfg = SimCfg()
    apply_overrides(cfg, args)

    for f in args.fig:
        if f not in FIG_RUNNERS:
            raise SystemExit(f"Unknown fig {f}. Available: {sorted(FIG_RUNNERS)}")

        print(f"=== RUN FIG {f} on {args.device} ===")

        if f == "2":
            FIG_RUNNERS[f](cfg, device=args.device, vs=args.vs,
                           rho_min=args.rho_min, rho_max=args.rho_max, rho_steps=args.rho_steps,
                           out=args.out)

        elif f == "3":
            FIG_RUNNERS[f](cfg, device=args.device, rho=args.rho, vs=args.vs,
                           out_headway=args.out_headway, out_velocity=args.out_velocity)

        elif f in ["4", "9"]:
            FIG_RUNNERS[f](cfg,
                           rho_min=args.rho_min, rho_max=args.rho_max, rho_steps=args.rho_steps,
                           vmax_list=args.vmax_list,
                           out=args.out)

        elif f == "5":
            FIG_RUNNERS[f](cfg, device=args.device, vs=args.vs,
                           out=args.out)
        
        elif f == "6":
            FIG_RUNNERS[f](cfg, device=args.device, vs=args.vs,
                           rho=args.rho,
                           rho_min=args.rho_min, rho_max=args.rho_max, rho_steps=args.rho_steps,
                           out_profile=args.out_profile, out_ratio=args.out_ratio)

        elif f == "7":
            FIG_RUNNERS[f](cfg, device=args.device, vs=args.vs,
                           rho_min=args.rho_min, rho_max=args.rho_max, rho_steps=args.rho_steps,
                           out_a=args.out_a, out_b=args.out_b)


        elif f == "8":
            FIG_RUNNERS[f](cfg, device=args.device, vs1=args.vs1, vs2=args.vs2,
                           out_prefix=args.out_prefix)

        elif f == "10":
            FIG_RUNNERS[f](cfg, device=args.device, vs=args.vs,
                           out_a=args.out_a, out_b=args.out_b)

if __name__ == "__main__":
    main()
