#!/bin/bash

MODE=$1
DOMAIN=$2

declare -a StringArray=( "GPT-2" "SC-GPT" "AUG-GPT" "AUG-GPT-SC" )
for model in ${StringArray[@]};
do
	cp result_woz.$model/results_${DOMAIN}.json ./
	sh evaluate.sh ${DOMAIN}
	mv tmp.log.bleu tmp.log.bleu.$model
done

python qualitative.py $MODE
