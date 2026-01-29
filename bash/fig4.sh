#!/bin/bash
python ../run.py \
  --fig 4 \
  --rho_min 0.01 --rho_max 0.8 --rho_steps 300 \
  --vmax_list 2.0 1.5 1.0 \
  --out fig4_theory_current.png
