#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 2 \
  --device cuda:0 \
  --vs 1.0 \
  --rho_min 0.02 --rho_max 0.8 --rho_steps 60 \
  --t_warmup 1000 --t_total 5000 --sample_every 20\
  --out fig2_current_vs_density.png