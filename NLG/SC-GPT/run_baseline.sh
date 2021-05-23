#!/bin/bash
export CUDA_VISIBLE_DEVICES=3

declare -a StringArray=( "sgd_movies" "sgd_weather" )

for DOMAIN in ${StringArray[@]};
do
	sh train_gpt2.sh $DOMAIN
	#sh train_scgpt.sh $DOMAIN
	sh decode.sh $DOMAIN
	sh evaluate_bleu.sh $DOMAIN > $DOMAIN.bleu
done
