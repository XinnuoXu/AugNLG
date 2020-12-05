export CUDA_VISIBLE_DEVICES=1

#EPOCH=20
#DOMAIN=taxi
#DOMAIN=train
#DOMAIN=tv
#DOMAIN=hotel
#DOMAIN=laptop
#DOMAIN=restaurant
#DOMAIN=attraction
#PRE_TRAINED_MODEL_PATH=./scgpt #gpt2

EPOCH=10
LR=1e-5
DOMAIN=$1
PRE_TRAINED_MODEL_PATH=./scgpt
MODEL_SAVE_PATH=./models.${DOMAIN}/

mkdir ./data/${DOMAIN}/./models.${DOMAIN}/
mkdir ${MODEL_SAVE_PATH}

python train.py \
	--output_dir=${MODEL_SAVE_PATH} \
	--model_type=gpt2 \
	--do_train \
	--do_eval \
	--model_name_or_path=${PRE_TRAINED_MODEL_PATH} \
	--eval_data_file=data/${DOMAIN}/train.txt \
	--per_gpu_train_batch_size 1 \
	--num_train_epochs ${EPOCH} \
	--learning_rate ${LR} \
	--overwrite_cache \
	--use_tokenize \
	--train_data_file=data/${DOMAIN}/train.txt \
	--overwrite_output_dir
