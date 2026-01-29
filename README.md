# Traffic-Jam Research — Mathematical Modelling (OVM with Slowdown Sections)

**Abstract.** This repository provides a reproducible research pipeline for studying traffic jam formation using the Optimal Velocity Model (OVM) with slowdown sections. It supports simulations across densities, measures current \(J\) vs. density \(p\), analyzes spatial structure (velocity/headway vs. position), estimates jam length ratios, and compares simulation results with theoretical curves. The workflow targets students and researchers who need reliable experiments and publication-ready figures.

---

## Table of Contents
- [Scientific Background](#scientific-background)
- [Reproducible Pipeline](#reproducible-pipeline)
- [Proposed Folder Structure](#proposed-folder-structure)
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
- **Optimal Velocity Model (OVM):** A car-following model where each vehicle accelerates toward an “optimal” speed based on its headway (distance to the vehicle ahead).
- **Slowdown sections:** Road segments with reduced desired speed to model bottlenecks or road conditions. These can trigger stop-and-go waves and jams.
- **Density \(p\):** Vehicle density on the ring road (vehicles per unit length). Increasing \(p\) can push the system from free flow to congested regimes.
- **Current \(J\):** Flow rate (vehicles per unit time). The \(J\)–\(p\) relationship (fundamental diagram) reveals phase transitions and capacity drops.

No heavy equations are required for interpretation; this repository focuses on intuitive, reproducible analysis.

---

## Reproducible Pipeline
1) **Simulate** OVM with configurable slowdown sections  
2) **Aggregate metrics** (current \(J\), mean speed, jam length ratio, etc.)  
3) **Plot** figures (PNG, optional MP4)  
4) **Export** runs to `/runs` with logs and metadata  

---

## Proposed Folder Structure
If your current repo is flat, consider migrating to the following structure for clarity and reproducibility:

```
traffic-jam-research-mathematical-modelling-/
├─ configs/
│  ├─ fig2.yaml
│  ├─ fig3.yaml
│  ├─ fig10.yaml
│  └─ sweep.yaml
├─ src/
│  ├─ model_ovm.py
│  ├─ sim.py
│  ├─ metrics.py
│  └─ road.py
├─ scripts/
│  ├─ run_sim.py
│  ├─ sweep_density.py
│  └─ plot_results.py
├─ data/                     # optional input datasets
├─ runs/                     # experiment outputs
├─ notebooks/                # exploratory analysis
├─ assets/                   # figures for README/papers
├─ requirements.txt
└─ README.md
```

> TODO: If your repo does not yet contain `configs/` or `scripts/`, create them or adapt the commands below to existing entry points (e.g., `run.py`).

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
Copy-paste examples (update paths if your scripts differ):

```bash
# Run a single experiment (e.g., Fig 2 config)
python scripts/run_sim.py --config configs/fig2.yaml

# Sweep density p values and collect J vs p
python scripts/sweep_density.py --config configs/sweep.yaml

# Plot results from a specific run directory
python scripts/plot_results.py --run runs/exp_001
```

> TODO: If `scripts/` does not exist, use the equivalent entry points (e.g., `python run.py`) and adjust arguments accordingly.

---

## Configuration
Example YAML (extend as needed):

```yaml
# configs/fig2.yaml
road_length: 4000           # total length of ring road
num_vehicles: 200           # N
sensitivity_a: 1.0          # response rate
vmax: 2.0                   # max speed in normal sections

# Slowdown sections
slowdown_lengths:
  LN: 200                   # length of normal section before slowdown
  LS: 200                   # length of slowdown section
vs_max: 0.5                 # max speed in slowdown section

# Simulation controls
dt: 0.1                     # timestep
steps: 50000                # number of integration steps
seed: 42                    # RNG seed for reproducibility
```

---

## Inputs & Outputs

### Inputs
- **Config YAML** (see above)  
  Contains road length, number of vehicles, OVM parameters, slowdown parameters, and simulation settings.

### Outputs
- **Metrics**: JSON/CSV logs with run metadata and aggregated statistics.
  Example schema (fields may vary; extend as needed):
  ```json
  {
    "run_id": "exp_001",
    "density_p": 0.05,
    "current_J": 0.12,
    "mean_speed": 1.25,
    "jam_length_ratio": 0.18,
    "seed": 42,
    "steps": 50000
  }
  ```

- **Plots (PNG)**:
  - `fig2_J_vs_p.png`
  - `fig3_spatial_structure.png`
  - `fig10_jam_length_vs_sections.png`
- **Optional videos (MP4)**:
  - `traj_exp_001.mp4`

> TODO: Align filenames with your plotting scripts if they differ.

---

## Reproducing Results

### Fig 2 — Current \(J\) vs Density \(p\)
```bash
python scripts/sweep_density.py --config configs/sweep.yaml
python scripts/plot_results.py --run runs/exp_sweep
```

### Fig 3 — Spatial Structure (velocity/headway vs position)
```bash
python scripts/run_sim.py --config configs/fig3.yaml
python scripts/plot_results.py --run runs/exp_fig3
```

### Fig 10 — Three Slowdown Sections + Jam Length Ratio
```bash
python scripts/run_sim.py --config configs/fig10.yaml
python scripts/plot_results.py --run runs/exp_fig10
```

---

## Troubleshooting
- **Numerical instability / exploding speeds**
  - Reduce `dt` (time step).
  - Ensure `sensitivity_a` and `vmax` are within stable regimes.
- **Performance**
  - Prefer vectorized operations in core loops.
  - Reduce `steps` or downsample logging for long sweeps.

---

## Citation
**How to cite:**  
If you use this repository in academic work, please cite it as below and include the specific commit hash.

```bibtex
@software{traffic_jam_ovm_2026,
  title        = {Traffic-Jam Research — Mathematical Modelling (OVM with Slowdown Sections)},
  author       = {La Minh Trung},
  year         = {2026},
  url          = {TODO: repository URL},
  version      = {TODO: commit hash or tag}
}
```

---

## License
TODO: Add a license file (e.g., MIT, BSD-3-Clause, Apache-2.0).

---

## Contact / Maintainer
**Lã Minh Trung**
