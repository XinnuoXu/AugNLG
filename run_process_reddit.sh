#!/bin/bash

REDDIT_PATH='/scratch/xxu/reddit/'
UTT_PATH='./reddit.utterances'
DELEX_PATH='./reddit.delex'

python process_reddit.py \
	-mode read_raw \
	-base_path ${REDDIT_PATH} \
	-utterance_path ${UTT_PATH} \
	-min_length 2 \
	-max_length 40

python process_reddit.py \
	-mode delexicalization \
	-utterance_path ${UTT_PATH} \
	-delex_path ${DELEX_PATH} 
