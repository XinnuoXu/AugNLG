#!/bin/bash

RAW_PATH=$1
TRAIN_PATH=$2

JSON_PATH=${TRAIN_PATH}.json/fsnlg

python preprocess.py \
	-mode format_text_to_json \
	-raw_path ${RAW_PATH} \
	-save_path ${JSON_PATH} \
	-shard_size 10000 \
	-n_cpus 30 \
	-log_file ../logs/cnndm.log \
