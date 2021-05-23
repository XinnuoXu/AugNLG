#!/bin/bash

DOMAIN=$1
MODE=random

declare -a StringArray=( "GPT-2" "AUG-GPT" )
for model in ${StringArray[@]};
do
	cp result_sgd.$model/results_${DOMAIN}.json ./
	sh evaluate_bleu.sh ${DOMAIN}
	mv tmp.log.bleu tmp.log.bleu.$model
done

python qualitative.py $MODE
mv tmp.sample tmp.sample.$DOMAIN
