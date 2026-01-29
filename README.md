# Traffic-Jam Research — Mathematical Modelling (OVM with Slowdown Sections)

Basic simulation code for traffic-jam formation using the Optimal Velocity Model (OVM) on a ring road with slowdown sections. The repository generates figure-style outputs (PNG) for fundamental diagrams, spatial profiles, and jam-length ratios, following experiments in the `experiments/` folder.

## Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [Experiments (Fig 2–10)](#experiments-fig-210)
- [Key Parameters](#key-parameters)
- [Outputs](#outputs)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Maintainer](#maintainer)

## Overview
This project simulates OVM dynamics with piecewise road segments:
- **Normal sections (N)** with max speed `vf_max`
- **Slowdown sections (S)** with lower max speed `vs`

It supports:
- Fundamental diagram: current `J` vs density `rho` (Fig 2)
- Spatial headway/velocity profiles (Fig 3, Fig 6, Fig 8)
- Jam-length ratios across layouts (Fig 5–8, Fig 10)
- Theoretical current curves (Fig 4, Fig 9)

## Requirements
- Ubuntu 22.04 (tested target)
- Python 3.10+ recommended
- Python packages: `numpy`, `matplotlib`, `tqdm`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
.
├─ run.py                  # CLI entry point for figure experiments
├─ config.py               # SimCfg default parameters
├─ sim.py                  # OVM time integration (RK4)
├─ model_ovm.py            # optimal velocity function
├─ road.py                 # road and segment definitions
├─ metrics.py              # jam-length utilities (optional)
├─ experiments/            # Fig 2–10 experiment scripts
└─ bash/                   # helper scripts to reproduce figures
```

## Quickstart
Run a single figure experiment directly:
```bash
python run.py --fig 3 --rho 0.25 --vs 1.0 \
  --out_headway fig3_headway_profile.png \
  --out_velocity fig3_velocity_profile.png
```

Fundamental diagram sweep (Fig 2):
```bash
python run.py --fig 2 --rho_min 0.02 --rho_max 0.80 --rho_steps 60 \
  --vs 1.0 --out fig2_current_vs_density.png
```

## Experiments (Fig 2–10)
The main entry point is `run.py` with `--fig` arguments. Available figures:

- `--fig 2` Fundamental diagram (simulation + theory)
- `--fig 3` Headway and velocity profiles (spatial structure)
- `--fig 4` Theoretical current curves (multiple `vmax`)
- `--fig 5` Jam-length ratio with two equal slowdowns
- `--fig 6` Unequal slowdown lengths (profile + ratio)
- `--fig 7` Alternative layouts (ratio)
- `--fig 8` Strongest slowdown study (profiles + ratio)
- `--fig 9` Theoretical saturated current
- `--fig 10` Three slowdown sections (equal/unequal)

Example using the helper scripts in `bash/` (GPU optional):
```bash
cd bash
./fig2.sh          # Fig 2: current vs density
./fig3.sh          # Fig 3: headway + velocity profiles
./fig10.sh         # Fig 10: jam-length ratios
```

## Key Parameters
Defaults are defined in `config.py` (`SimCfg`), and can be overridden via CLI:

- `N`: number of vehicles
- `a_sens`: sensitivity in dv/dt = a(V - v)
- `vf_max`: max speed in normal sections
- `alpha_ov`, `x_f_c`, `x_s_c`: OVM parameters
- `dt`, `t_warmup`, `t_total`, `sample_every`
- `dx_threshold`: jam detection threshold
- `rho`, `vs`, `vs1`, `vs2`: density and slowdown speeds

Example overrides:
```bash
python run.py --fig 2 --N 400 --a_sens 2.0 --vf_max 2.2 --dt 0.0078125
```

## Outputs
Outputs are PNG files saved to the paths you pass via CLI, e.g.:
- `fig2_current_vs_density.png`
- `fig3_headway_profile.png`
- `fig3_velocity_profile.png`
- `fig10a_jam_ratio.png`, `fig10b_jam_ratio.png`

## Maintainer
Lã Minh Trung
