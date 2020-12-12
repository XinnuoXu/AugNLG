# AUG-NLG (Augmented NLG)

This repository is forked from `pengbaolin/SC-GPT` for paper [Few-shot Natural Language Generation for Task-Oriented Dialog](https://arxiv.org/abs/2002.12328)


## Dataset: FewShotWoz

### Data path

Oritinal [FewshotWoz](https://arxiv.org/abs/2002.12328) and FewshotSGD data are in directory `./data_original/`. Augmented data is in directory `./data_augmentation/`. Specifically,

* Oritinal FewshotWoz data is in directory ./data_original/FewShotWoz/
* Oritinal FewshotSGD data is in directory ./data_original/SGD/
* Augmented data for FewshotWoz:
  * pre-trainning AUG-GPT is in directory ./data_augmentation/FewShotWoz.self-learning/


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
* `GPT-2`: Fine-tune GPT-2 with few-shot in-domain NLG examples. Run `sh train_gpt2.sh {domain}`
* `SC-GPT`: Fine-tune GPT-2 with (1) dialogue data from other domains (2) few-shot in-domain examples 
  - Fetch and unzip the checkpoint for fine-tuning (1)
    ```bash
    wget https://bapengstorage.blob.core.windows.net/fileshare/scgpt.tar.gz
    tar -xvf scgpt.tar.gz
    ```
  - Run the fine-tuning (2) `sh train_scgpt.sh {domain}`

### AUG-NLG training
* Step1: Fine-tune GPT-2 with Reddit-augmented examples. Run `sh pre_train.sh {domain}`
* Step2: Fine-tune model from step1 with few-shot in-domain NLG examples. Run `sh train.sh {domain}`

### Decoding
Training checkpoints are stored in directory `models.{domain}`. To decode (inference) all models run `sh decode.sh {domain}`. You can find the decoding results in file `results_{domain}.json`.

### Evaluation
To evaluate the output, run `sh evaluate.sh {domain}`

*script for attraction/train/taxi will be provided soon*

