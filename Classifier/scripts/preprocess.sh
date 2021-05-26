#!/bin/bash

TRAIN_PATH=$1
JSON_PATH=${TRAIN_PATH}.json/
BERT_DATA_PATH=${TRAIN_PATH}.data/

python preprocess.py \
	-mode format_to_bert \
	-raw_path ${JSON_PATH} \
	-save_path ${BERT_DATA_PATH} \
      	-lower \
	-n_cpus 30 \
	-log_file ../logs/preprocess.log
