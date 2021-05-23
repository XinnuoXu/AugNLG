# AugNLG

Code for paper "*Xinnuo Xu, Guoyin Wang, Young-Bum Kim, Sungjin Lee* [AUGNLG: Few-shot Natural Language Generation using Self-trainedData Augmentation](https://github.com/XinnuoXu/AugNLG)" *Proceedings of [ACL 2021](https://2021.aclweb.org)* :tada: :tada: :tada:

## Environment setup

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

## Data
Follow the instruction [here](https://github.com/PolyAI-LDN/conversational-datasets/tree/master/reddit) to download the reddit data.
