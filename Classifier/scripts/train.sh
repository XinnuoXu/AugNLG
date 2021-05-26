#!/bin/bash

TRAIN_PATH=$1
BERT_DATA_PATH=${TRAIN_PATH}.data/fsnlg
MODEL_PATH=${TRAIN_PATH}.models/

python train.py  \
	-mode train \
	-bert_data_path ${BERT_DATA_PATH} \
	-model_path ${MODEL_PATH} \
	-lr 0.002 \
	-save_checkpoint_steps 100 \
	-batch_size 140 \
	-warmup_steps 50 \
	-train_steps 500 \
	-report_every 25 \
	-accum_count 5 \
	-seed 777 \
	-visible_gpus 0,1,3 \
	-log_file ../logs/abs_bert_cnndm
