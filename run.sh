#!/bin/bash

DOMAIN=$1
DELEX_PATH='./reddit.delex'

# retrive in-domain keywords and reddit utterances
python key_ngrams.py -domain ${DOMAIN} -delex_path ${DELEX_PATH} -ngrams 2
python key_augs.py -domain ${DOMAIN} -delex_path ${DELEX_PATH}
#sh run_rtv.sh ${DOMAIN}

# get pre-train utterances using self-learning
#sh run_sl.sh ${DOMAIN}

# label augmented data with NLU
#sh run_nlu.sh ${DOMAIN}

# pre-train and fine-tune NLG
#sh run_nlg.sh ${DOMAIN}
