#!/bin/bash
python ../run.py \
  --fig 9 \
  --rho_min 0.01 --rho_max 0.8 --rho_steps 300 \
  --vmax_list 2.0 1.0 0.8 \
  --out fig9_saturated_current.png
