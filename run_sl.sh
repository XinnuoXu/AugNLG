#!/bin/bash

DOMAIN=$1

source ~/anaconda3/etc/profile.d/conda.sh
#conda activate FS_NLG
conda activate gpt


# self learning for classifier
python self_learning.py $DOMAIN

# get the final augmented data
#python get_aug_from_classifier.py $DOMAIN

