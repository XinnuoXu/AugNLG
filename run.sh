#!/bin/bash

DOMAIN=$1

# retrive in-domain keywords and reddit utterances
sh run_rtv.sh ${DOMAIN}

# get pre-train utterances using self-learning
sh run_sl.sh ${DOMAIN}

# label augmented data with NLU
sh run_nlu.sh ${DOMAIN}

# pre-train and fine-tune NLG
sh run_nlg.sh ${DOMAIN}
