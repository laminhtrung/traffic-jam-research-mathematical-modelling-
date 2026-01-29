#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 10 \
  --device cuda:0 \
  --vs 1.0 \
  --out_a fig10a_jam_ratio.png \
  --out_b fig10b_jam_ratio.png
