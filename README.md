# SC-GPT

This repository is forked from `pengbaolin/SC-GPT` for the following paper:

[Few-shot Natural Language Generation for Task-Oriented Dialog](https://arxiv.org/abs/2002.12328)
Baolin Peng, Chenguang Zhu, Chunyuan Li, Xiujun Li, Jinchao Li, Michael Zeng and Jianfeng Gao


## Dataset: FewShotWoz
*FewShotWoz* is constructed using dataset from RNNLG and MultiWoz.

**Data files includes** 

<code>{domain}/train.json</code>: training set in json format used for evaluation, other package like RNNLG also need this format.
<code>{domain}/train.txt</code>: linearized training set for GPT-2 models.
<code>{domain}/test.json</code>: testing set in json format.
<code>{domain}/test.txt</code>: linearized testing set for GPT-2 models.

**Data format**
```json
[
"inform(name='hakka restaurant';pricerange=moderate)", 
"hakka restaurant is moderate -ly priced", 
"hakka restaurant is moderate -ly priced" 
]

First item: dialog act
Second item: corresponding natural language description
Thrid item: repeated for evaluation script

Linearized as:
inform ( name = hakka restaurant ; pricerange = moderate ) & hakka restaurant is moderate -ly priced
```

## Pipeline
*The code is still under cleanup. More details of code usage will be added soon*

**Setup**

Please use the below command to clone and install the requirements.
```bash
git clone https://github.com/pengbaolin/SC-GPT.git
cd SC-GPT
pip install -r requirements.txt
```
Fetch and unzip the checkpoint
```bash
wget https://bapengstorage.blob.core.windows.net/fileshare/scgpt.tar.gz
tar -xvf scgpt.tar.gz
```
**Training**
```bash
export CUDA_VISIBLE_DEVICES=0
python train.py --output_dir=MODEL_SAVE_PATH --model_type=gpt2 --model_name_or_path=PRE_TRINED_MODEL_PATH --do_train --do_eval --eval_data_file=data/restaurant/train.txt --per_gpu_train_batch_size 1 --num_train_epochs EPOCH --learning_rate LR --overwrite_cache --use_tokenize --train_data_file=data/restaurant/train.txt --overwrite_output_dir
```
<code>MODEL_SAVE_PATH </code>: Path of the saving model .

<code>PRE_TRAINED_MODEL_PATH </code>: Initial checkpoint; Could start from gpt2, gpt2-meidum or our provided scgpt folder.

<code>EPOCH </code>: Number of training epochs;  5 is enough for a reasonable performance

<code>LR </code>: Learning rate; 5e-5, 1e-5, or 1e-4

**Decoding**
```bash
export CUDA_VISIBLE_DEVICES=0
python generate.py --model_type=gpt2 --model_name_or_path=MODEL_SAVE_PATH --num_samples 5 --input_file=data/restaurant/test.txt --top_k 5 --output_file=results.json --length 80
```

**Evaluate**
```bash
python evaluator.py --domain restaurant results.json
```
*script for attraction/train/taxi will be provided soon*

