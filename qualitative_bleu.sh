#!/bin/bash

DOMAIN=$1
MODE=bleu_better

declare -a StringArray=( "GPT-2" "SC-GPT" "AUG-GPT" "AUG-GPT-SC" )
for model in ${StringArray[@]};
do
	cp result_woz.$model/results_${DOMAIN}.json ./
	sh evaluate_bleu.sh ${DOMAIN}
	mv tmp.log.bleu tmp.log.bleu.$model
done

python qualitative.py $MODE
