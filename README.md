# Traffic-Jam Research — Mathematical Modelling (OVM with Slowdown Sections)

**Abstract.** This repository provides a reproducible pipeline for studying traffic jam formation with the Optimal Velocity Model (OVM) and slowdown sections. It supports fundamental-diagram analysis (current \(J\) vs density \(\rho\)), spatial profiles of headway/velocity, jam-length ratios in normal sections, and comparisons between simulation and theoretical curves. It is designed for students and researchers who need reproducible experiments and publication-ready figures.

---

## Table of Contents
- [Scientific Background](#scientific-background)
- [Reproducible Pipeline](#reproducible-pipeline)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Inputs & Outputs](#inputs--outputs)
- [Reproducing Results](#reproducing-results)
- [Troubleshooting](#troubleshooting)
- [Citation](#citation)
- [License](#license)
- [Contact / Maintainer](#contact--maintainer)

---

## Scientific Background
- **Optimal Velocity Model (OVM):** A car-following model where each vehicle accelerates toward an “optimal” speed based on headway (distance to the vehicle ahead).
- **Slowdown sections:** Road segments with reduced desired speed, modeling bottlenecks or road conditions that can trigger stop-and-go waves.
- **Density \(\rho\):** Vehicles per unit road length on a ring road. Increasing \(\rho\) can drive transitions from free flow to congestion.
- **Current \(J\):** Flow rate (vehicles per unit time). The \(J\)–\(\rho\) curve reveals capacity limits and phase transitions.

This repo focuses on intuitive interpretation and reproducible figure generation rather than heavy derivations.

---

## Reproducible Pipeline
1) **Simulate** OVM dynamics on a ring road with slowdown sections  
2) **Aggregate metrics** (mean speed, current \(J\), jam ratios)  
3) **Plot** figures (PNG)  
4) **Export** outputs to a user-specified path  

---

## Repository Structure

### Current structure
```
traffic-jam-research-mathematical-modelling-/
├─ experiments/
│  ├─ fig2_fundamental.py
│  ├─ fig3_profile.py
│  ├─ fig4_9_theory_current.py
│  ├─ fig5_jam_ratio_equal.py
│  ├─ fig6_jam_ratio_unequal.py
│  ├─ fig7_various_layouts.py
│  ├─ fig8_strongest_slowdown.py
│  └─ fig10_three_slowdowns.py
├─ config.py
├─ metrics.py
├─ model_ovm.py
├─ road.py
├─ run.py
├─ sim.py
└─ requirements.txt
```

---

## Installation
Ubuntu 22.04, Python 3.10+ recommended.

```bash
conda create -n ovm-traffic python=3.10 -y
conda activate ovm-traffic
pip install -r requirements.txt
```

---

## Quickstart

### Run a single experiment
```bash
python run.py --fig 3 --rho 0.25 --vs 1.0 \
  --out_headway fig3_headway.png \
  --out_velocity fig3_velocity.png
```

### Sweep density \(\rho\) values (fundamental diagram)
```bash
python run.py --fig 2 --rho_min 0.02 --rho_max 0.80 --rho_steps 60 \
  --vs 1.0 --out fig2_current_vs_density.png
```

### Generate Fig 10-style jam-length ratios (three slowdowns)
```bash
python run.py --fig 10 --rho_min 0.18 --rho_max 0.35 --rho_steps 18 \
  --vs 1.0 --out_a fig10a_jam_ratio.png --out_b fig10b_jam_ratio.png
```

### Export results to a `/runs` directory
```bash
mkdir -p runs
python run.py --fig 2 --rho_min 0.02 --rho_max 0.80 --rho_steps 60 \
  --vs 1.0 --out runs/fig2_current_vs_density.png
```

---

## Configuration
This project is configured via the `SimCfg` dataclass in `config.py`, with CLI overrides in `run.py`.

**Defaults (from `config.py`):**
- `N` (vehicles)
- `a_sens` (sensitivity)
- `vf_max` (normal-section max speed)
- `alpha_ov`, `x_f_c`, `x_s_c` (OVM parameters)
- `dt`, `t_warmup`, `t_total`, `sample_every`
- `dx_threshold` (jam detection)
- `seed`

**Override examples (CLI):**
```bash
python run.py --fig 2 --N 400 --a_sens 2.0 --vf_max 2.2 --dt 0.0078125
```

> TODO: YAML-based configuration is not implemented yet. If needed, add a config loader and pass values into `SimCfg`.

---

## Inputs & Outputs

### Inputs
- **CLI arguments** to `run.py` select figures and override parameters.
- **Simulation parameters** are defined in `config.py`.

### Outputs
- **Figures (PNG)** saved to user-specified paths:
  - Fig 2: `--out` (default: `fig2_current_vs_density.png`)
  - Fig 3: `--out_headway`, `--out_velocity`
  - Fig 10: `--out_a`, `--out_b`

> TODO: Structured logs (JSON/CSV) are not currently emitted. Add logging if you need machine-readable results for downstream analysis.

---

## Reproducing Results

### Fig 2 — Current \(J\) vs Density \(\rho\)
```bash
python run.py --fig 2 --rho_min 0.02 --rho_max 0.80 --rho_steps 60 \
  --vs 1.0 --out fig2_current_vs_density.png
```

### Fig 3 — Spatial structure (headway/velocity vs position)
```bash
python run.py --fig 3 --rho 0.25 --vs 1.0 \
  --out_headway fig3_headway.png \
  --out_velocity fig3_velocity.png
```

### Fig 10 — Three slowdown sections + jam-length ratios
```bash
python run.py --fig 10 --rho_min 0.18 --rho_max 0.35 --rho_steps 18 \
  --vs 1.0 --out_a fig10a_jam_ratio.png --out_b fig10b_jam_ratio.png
```

---

## Troubleshooting
- **Numerical instability / exploding speeds**
  - Reduce `dt`.
  - Keep `a_sens` and `vf_max` within stable regimes.
- **Performance**
  - Reduce `t_total` or increase `sample_every`.
  - Prefer GPU (`--device cuda`) if you have CUDA available; otherwise CPU is fine.

---


## Contact / Maintainer
**Lã Minh Trung**
