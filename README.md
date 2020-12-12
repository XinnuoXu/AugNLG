# AUG-NLG (Augmented NLG)

This repository is forked from `pengbaolin/SC-GPT` for paper [Few-shot Natural Language Generation for Task-Oriented Dialog](https://arxiv.org/abs/2002.12328)


## Dataset

Oritinal [FewshotWoz](https://arxiv.org/abs/2002.12328) and FewshotSGD data are in directory `./data_original/`. Augmented data is in directory `./data_augmentation/`. Specifically,

* Oritinal FewshotWoz data is in directories .`/data_original/FewShotWoz/{domain}`
* Oritinal FewshotSGD data is in directories `./data_original/SGD/{domain}`
* Augmented data for FewshotWoz:
  * Pre-training data for AUG-GPT is in directories `./data_augmentation/FewShotWoz.self-learning/{domain}.pre_train`
  * Pre-training data for SC-NLU is in directories `./data_augmentation/FewShotWoz.SC-NLU/{domain}.pre_train`
  * Pre-training data for SC-NLU+AUG is in directories `./data_augmentation/FewShotWoz.SC-NLU_AUG/{domain}.pre_train`
* Augmented data for FewshotSGD:
  * Pre-training data for AUG-GPT is in directories `./data_augmentation/FewShotSGD.self-learning/{domain}.pre_train`


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

### Data processing
Before training and pre-training, create a directory `./data/`. Move the oritinal data (directories under `/data_original/`) and the pre-training data (directories under `./data_augmentation/`) to `./data/`.

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

