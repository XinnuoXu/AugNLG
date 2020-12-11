#!/bin/bash

declare -a StringArray=( "sgd_movies" "sgd_music" "sgd_rentalcars" "sgd_ridesharing" "sgd_services" "sgd_travel" )


for DOMAIN in ${StringArray[@]};
do
	sh train_gpt2.sh $DOMAIN
	sh decode.sh $DOMAIN
	sh evaluate_bleu.sh $DOMAIN > $DOMAIN.bleu
done
