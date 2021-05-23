#!/bin/bash

DOMAIN=$1
DEVICE=$2

export CUDA_VISIBLE_DEVICES=$DEVICE

source ~/anaconda3/etc/profile.d/conda.sh
#conda activate FS_NLG
conda activate gpt
cd ./NLG/SC-GPT/

# pre-train NLG using augmented data
#sh pre_train.sh $DOMAIN

# fine-tune NLG
#sh train.sh $DOMAIN
#sh train_scgpt.sh $DOMAIN
sh train_gpt2.sh $DOMAIN

# test NLG
sh decode.sh $DOMAIN

# evaluate (domains in FewshotWoz)
#sh evaluate.sh $DOMAIN

# evaluate (domains in FewshotSGD)
#sh evaluate_bleu.sh $DOMAIN
