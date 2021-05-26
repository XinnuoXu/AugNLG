#!/bin/bash

DOMAIN=$1
BERT_DATA_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.data/fsnlg 
MODEL_PATH=/scratch/xxu/few_shot_nlg/${DOMAIN}.models/
RESULT_PATH=./data.${DOMAIN}/prediction.txt

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
awk -F"\t" 'FNR==1 {++fIndex} fIndex==1{if($2==1){aw[$1]=$2;need_recall+=1}} fIndex==2{if($2 in aw)if($1>0.5)recall+=1}END{print ("Round2 R:", recall/need_recall)}' data.${DOMAIN}/dev.txt data.${DOMAIN}/prediction.txt >> data.${DOMAIN}/res.txt
# Precision
awk -F"\t" 'FNR==1 {++fIndex} fIndex==1{if($2==1){aw[$1]}} fIndex==2{if($1>0.5){recall+=1; if($2 in aw){correct+=1}}}END{print("Round2 P:", correct/recall)}' data.${DOMAIN}/dev.txt data.${DOMAIN}/prediction.txt >> data.${DOMAIN}/res.txt
