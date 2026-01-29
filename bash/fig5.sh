CUDA_VISIBLE_DEVICES=0 python ../run.py \
  --fig 5 \
  --device cuda:0 \
  --vs 1.0 \
  --rho_min 0.15 --rho_max 0.35 --rho_steps 12 \
  --t_warmup 15000 --t_total 45000 --sample_every 50 \
  --out fig5_jam_length_ratio.png
