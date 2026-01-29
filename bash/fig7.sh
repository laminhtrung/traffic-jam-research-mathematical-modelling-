#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 7 \
  --device cuda:0 \
  --vs 1.0 \
  --rho_min 0.15 --rho_max 0.35 --rho_steps 15 \
  --t_warmup 15000 --t_total 45000 --sample_every 50 \
  --out_a fig7a_jam_length_ratio.png \
  --out_b fig7b_jam_length_ratio.png
