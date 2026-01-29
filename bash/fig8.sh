#!/bin/bash
GPU=${1:-0}
CUDA_VISIBLE_DEVICES=${GPU} python ../run.py \
  --fig 8 \
  --device cuda:0 \
  --vs1 1.5 --vs2 1.0 \
  --out_prefix fig8
