#!/bin/bash

RAW_PATH=$1
TRAIN_PATH=$2
BERT_DATA_PATH=${TRAIN_PATH}.data/fsnlg 
MODEL_PATH=${TRAIN_PATH}.models/
RESULT_PATH=./${RAW_PATH}/prediction.txt

# model steps: hotel=8000; restaurant/${DOMAIN}=20000

python train.py \
	-mode dev \
	-test_batch_size 500 \
	-bert_data_path ${BERT_DATA_PATH} \
	-log_file ../logs/val_abs_bert_cnndm \
	-test_from ${MODEL_PATH}model_step_20000.pt \
	-visible_gpus 0,2,1 \
	-result_path ${RESULT_PATH}

# Recall
awk -F"\t" 'FNR==1 {++fIndex} fIndex==1{if($2==1){aw[$1]=$2;need_recall+=1}} fIndex==2{if($2 in aw)if($1>0.5)recall+=1}END{print ("Round2 R:", recall/need_recall)}' ${RAW_PATH}/dev.txt ${RAW_PATH}/prediction.txt >> ${RAW_PATH}/res.txt
# Precision
awk -F"\t" 'FNR==1 {++fIndex} fIndex==1{if($2==1){aw[$1]}} fIndex==2{if($1>0.5){recall+=1; if($2 in aw){correct+=1}}}END{print("Round2 P:", correct/recall)}' ${RAW_PATH}/dev.txt ${RAW_PATH}/prediction.txt >> ${RAW_PATH}/res.txt
