# NLG_adaption

## Environment setup

### Step1: Clone the repo and update all submodules

```
git clone https://github.com/XinnuoXu/NLG_adaption.git
git submodule init
git submodule update

cd ./NLG/SC-GPT
git checkout master
```

### Step2: Initialize eenvironment

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
