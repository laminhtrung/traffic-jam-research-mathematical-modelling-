#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 3 \
  --device cuda:0 \
  --rho 0.25 \
  --vs 1.0 \
  --t_warmup 10000 --t_total 50000 --sample_every 20\
  --out_headway fig3_headway_profile.png \
  --out_velocity fig3_velocity_profile.png
