#!/bin/bash

DOMAIN=$1
ITERATION=$2

cp data.${DOMAIN}/train.txt data.${DOMAIN}/train_${ITERATION}.txt
sh reset_all.sh $DOMAIN
sh scripts/preprocess_json.sh $DOMAIN
sh scripts/preprocess.sh $DOMAIN
sh scripts/train_2round.sh $DOMAIN
sh scripts/dev_2round.sh $DOMAIN
sh scripts/test_2round.sh $DOMAIN
