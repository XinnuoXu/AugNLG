#!/bin/bash

TRAIN_PATH=$1

rm -r ${TRAIN_PATH}.json
rm -r ${TRAIN_PATH}.data
rm -r ${TRAIN_PATH}.models

mkdir ${TRAIN_PATH}.json
mkdir ${TRAIN_PATH}.data
mkdir ${TRAIN_PATH}.models
