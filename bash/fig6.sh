#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 6 \
  --device cuda:0 \
  --vs 1.0 \
  --rho 0.31 \
  --rho_min 0.15 --rho_max 0.35 --rho_steps 15 \
  --t_warmup 15000 --t_total 45000 --sample_every 50 \
  --out_profile fig6a_headway_profile.png \
  --out_ratio fig6b_jam_length_ratio.png
