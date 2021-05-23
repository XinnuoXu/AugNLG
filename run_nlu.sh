#!/bin/bash

DOMAIN=$1
UTT_BUCKET=${DOMAIN}'_system'

source ~/anaconda3/etc/profile.d/conda.sh
conda activate NLU

# get the final augmented data
python get_aug_from_classifier.py $DOMAIN

# prepare data for training/testing nlu
python nlg_to_nlu.py ${DOMAIN} ${UTT_BUCKET}
rm NLU/token-classification/nlu/*
python nlu_to_bert.py ${DOMAIN} -1 -1


# train (on few-shot in-domain data) and test (on pre-train utterances) nlu
cd ./NLU/token-classification/
sh run_nlu.sh
cd ../../
python nlu_to_nlg.py ${DOMAIN}

