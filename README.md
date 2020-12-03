# GPT-NLG

This repository is forked from `pengbaolin/SC-GPT` for paper [Few-shot Natural Language Generation for Task-Oriented Dialog](https://arxiv.org/abs/2002.12328)


## Dataset: FewShotWoz

### Data path

FewShotWoz data is in directory `./data/FewShotWoz/`. Original data from the [paper](https://arxiv.org/abs/2002.12328) is in sub-directories `./data/FewShotWoz/{domain}`. The Reddit-based augmentations are in `./data/FewShotWoz/{domain}.pre_train`.

### Data files includes

There are two `.txt` files in each sub-directory:
* <code>{domain}/train.txt</code>: linearized training set for GPT-2 models.
* <code>{domain}/test.txt</code>: linearized testing set for GPT-2 models.

### Data format

File `train.txt` and `test.txt` share the same format, `Linearized dialogue act & Correlated sentence`, for example:
```
inform ( name = hakka restaurant ; pricerange = moderate ) & hakka restaurant is moderate -ly priced
```

## Quickstart

### Baselines training
* `GPT-2`: Fine-tuning GPT-2 with few-shot in-domain NLG examples. Run `sh train_gpt2.sh {domain}`
* `SC-GPT`: Fine-tuning GPT-2 with 1) dialogue data from other domains 2) few-shot in-domain examples
  - Fetch and unzip the checkpoint for the first fine-tuning
    ```bash
    wget https://bapengstorage.blob.core.windows.net/fileshare/scgpt.tar.gz
    tar -xvf scgpt.tar.gz
    ```
  - Run the second fine-tuning `sh train_scgpt.sh {domain}`


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

