#!/bin/bash

TARGET_DIR=$1
TRAIN_DIR=$2

cp ${TARGET_DIR}/train.txt ${TARGET_DIR}/train_0.txt
sh reset_all.sh ${TRAIN_DIR}
echo 'DONE reset_all.sh'
sh scripts/preprocess_json.sh ${TARGET_DIR} ${TRAIN_DIR}
echo 'DONE preprocess_json.sh'
sh scripts/preprocess.sh ${TRAIN_DIR}
echo 'DONE preprocess.sh'
sh scripts/train.sh ${TRAIN_DIR}
sh scripts/dev.sh ${TARGET_DIR} ${TRAIN_DIR}
sh scripts/test.sh ${TARGET_DIR} ${TRAIN_DIR}
