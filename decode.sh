export CUDA_VISIBLE_DEVICES=0

#DOMAIN=taxi
#DOMAIN=train
#DOMAIN=tv
#DOMAIN=hotel
#DOMAIN=laptop
#DOMAIN=restaurant
#DOMAIN=attraction
DOMAIN=$1

MODEL_SAVE_PATH=./models.${DOMAIN}/
DATA_TYPE=FewShotWoz

python generate.py \
	--model_type=gpt2 \
	--model_name_or_path=${MODEL_SAVE_PATH} \
	--num_samples 5 \
	--input_file=data/${DATA_TYPE}/${DOMAIN}/test.txt \
	--top_p 0.5 \
	--output_file=results_${DOMAIN}.json \
	--length 80
