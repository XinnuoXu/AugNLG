export CUDA_VISIBLE_DEVICES=3

sh train_scgpt.sh $1
sh decode.sh $1
sh evaluate.sh $1
