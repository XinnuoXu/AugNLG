#!/bin/bash

TARGET_DIR=$1
TRAIN_DIR=$2
ITERATION=$3

cp ${TARGET_DIR}/train.txt ${TARGET_DIR}/train_${ITERATION}.txt
sh reset_all.sh ${TRAIN_DIR} 
sh scripts/preprocess_json.sh ${TARGET_DIR} ${TRAIN_DIR}
sh scripts/preprocess.sh ${TRAIN_DIR}
sh scripts/train_2round.sh ${TRAIN_DIR} 
sh scripts/dev_2round.sh ${TARGET_DIR} ${TRAIN_DIR}
sh scripts/test_2round.sh ${TARGET_DIR} ${TRAIN_DIR}
