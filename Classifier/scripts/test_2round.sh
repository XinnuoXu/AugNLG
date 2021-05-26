#!/bin/bash

DOMAIN=$1
BERT_DATA_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.data/fsnlg 
MODEL_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.models/
RESULT_PATH=./data.${DOMAIN}/prediction.txt

python train.py \
	-mode test \
	-test_batch_size 500 \
	-bert_data_path ${BERT_DATA_PATH} \
	-log_file ../logs/val_abs_bert_cnndm \
	-test_from ${MODEL_PATH}model_step_20000.pt \
	-visible_gpus 0,3,1 \
	-result_path ${RESULT_PATH}
