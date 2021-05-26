#!/bin/bash

DOMAIN=$1
BERT_DATA_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.data/fsnlg
MODEL_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.models/

python train.py  \
	-mode train \
	-bert_data_path ${BERT_DATA_PATH} \
	-model_path ${MODEL_PATH} \
	-lr 0.001 \
	-save_checkpoint_steps 4000 \
	-batch_size 140 \
	-warmup_steps 4000 \
	-train_steps 20000 \
	-report_every 50 \
	-accum_count 5 \
	-seed 777 \
	-visible_gpus 0,1,3 \
	-log_file ../logs/abs_bert_cnndm
