#!/bin/bash

RAW_PATH=$1
TRAIN_PATH=$2
BERT_DATA_PATH=${TRAIN_PATH}.data/fsnlg 
MODEL_PATH=${TRAIN_PATH}.models/
RESULT_PATH=./${RAW_PATH}/prediction.txt

python train.py \
	-mode test \
	-test_batch_size 500 \
	-bert_data_path ${BERT_DATA_PATH} \
	-log_file ../logs/val_abs_bert_cnndm \
	-test_from ${MODEL_PATH}model_step_500.pt \
	-visible_gpus 0,3,1 \
	-result_path ${RESULT_PATH}
