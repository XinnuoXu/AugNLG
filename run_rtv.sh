#!/bin/bash

DOMAIN=$1

source ~/anaconda3/etc/profile.d/conda.sh
conda activate FS_NLG

# get ngram from seed utterances
python key_ngrams.py ${DOMAIN}

# augment utterances from reddit data
python key_augs.py ${DOMAIN}
