# AugNLG

Code for paper "*Xinnuo Xu, Guoyin Wang, Young-Bum Kim, Sungjin Lee* [AUGNLG: Few-shot Natural Language Generation using Self-trainedData Augmentation](https://github.com/XinnuoXu/AugNLG)" *Proceedings of [ACL 2021](https://2021.aclweb.org)* main conference :tada: :tada: :tada:

This work introduce **AugNLG**, a novel data augmentation approach that combines a self-trained neural retrieval model with a few-shot learned NLU model, to automatically create MR-to-Text data from open-domain texts. The overall pipeline for the data augmentation is shown as:

![Frame.jpg](https://github.com/XinnuoXu/AugNLG/blob/master/Frame.jpg)

## :seedling: Environment setup

### Step1: Clone the repo and update all submodules

```
git clone https://github.com/XinnuoXu/AugNLG.git
git submodule init
git submodule update

cd ./NLG/SC-GPT
git checkout public
```

### Step2: Initialize environment

```
conda create -n FS_NLG python=3.6
conda activate FS_NLG
pip install -r requirements.txt
```

```
conda create -n NLU python=3.6
conda activate NLU
conda install pytorch torchvision torchaudio cudatoolkit=10.1 -c pytorch
conda install -c huggingface transformers
pip install conllu
install importlib_metadata
pip install nltk
pip install wordsegment
```


## :seedling: Data Resource
Follow the instruction [here](https://github.com/PolyAI-LDN/conversational-datasets/tree/master/reddit) to download the reddit data. To process the downloaded reddit data with referenced hyper-parameters, directly run:
```
sh run_process_reddit.sh
```

The script includes two sub-steps: 

* **Extract utterances from the original reddit data**
```
python process_reddit.py -base_path [your_reddit_dir] -utterance_path [where_to_save_the_utterances] -mode read_raw -min_length [min_token_num_per_utterance] -max_length [max_token_num_per_utterance] -thread_num [thread_num_for_processing]
```

* **Delexicalize the utterances**
```
python process_reddit.py -utterance_path [where_you_saved_the_utterances] -delex_path [where_to_save_the_delexed_utterances] -mode delexicalization -thread_num [thread_num_for_processing]
```

The outcome of the delexicalization (*-delex_path*) is 2️⃣ in the overall pipeline. Meanwhile, Fewshot NLG Data (*FewShotWOZ* and *FewShotSGD*, 1️⃣ in the overall pipeline) can be found in `./domains`, with no extra processing.


## :seedling: Data Augmentation for domains
To augment data for a certain domain with referenced hyper-parameters, directly run (available *[domain_name]* can be found in `./domains`):
```
sh ./run.sh [domain_name]
```

The script includes multiple sub-steps: 

* **Extract keywords from in-domain utterances**
```
python key_ngrams.py -domain [domain_name] -delex_path [where_you_saved_the_delexed_utterances] -thread_num [thread_num_for_processing] -min_count [minimum_times_phrases_appear_in_corpus] -min_tf_idf [tf_idf_threshold]
```
The output is file `./augmented_data/[domain_name]_system.kws`.
 
* **Retrive candidate utterances** 
```
python key_augs.py -domain [domain_name] -delex_path [where_you_saved_the_delexed_utterances] -thread_num [thread_num_for_processing]
```
The output is 3️⃣ in the overall pipeline, which is saved in directory `./augmented_data/[domain_name].aug/`.

