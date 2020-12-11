import numpy as np
import os
import operator
from math import sqrt
import random
from ast import literal_eval
import pickle
from copy import deepcopy
import argparse

from utils.loader.DataReader import *
from utils.loader.GentScorer import *
from nltk.tokenize import sent_tokenize, word_tokenize

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)
np.set_printoptions(precision=4)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=None, type=str, required=True, help="Please specify a domain")
    parser.add_argument("--target_file", default=None, type=str, required=True, help="Please specify the result file")
    args = parser.parse_args()

    domain = args.domain
    target_file = args.target_file

    train       = f'data/{domain}/train.json'
    valid       = f'data/{domain}/train.json'
    test        = f'data/{domain}/test.json'
    vocab       = 'utils/resource/vocab'
    detectpairs = 'utils/resource/detect.pair'

    gentscorer = GentScorer(detectpairs)
    results_from_gpt = json.load(open(target_file))
    gold_json = json.load(open(test))
    parallel_corpus, hdc_corpus = [], []
    for idx in range(len(results_from_gpt)):
        gold_strs = [gold_json[idx][1]]
        gen_strs = results_from_gpt[idx]
        gen_strs_single = []
        gen_strs_ = []
        for gen_str in gen_strs:
            cl_idx = gen_str.find('<|endoftext|>')
            gen_str = gen_str[:cl_idx].strip().lower()
            gen_str = ' '.join(word_tokenize(gen_str))
            gen_str.replace('-s','')
            gen_str = gen_str.replace('watts','watt -s').replace('televisions','television -s').replace('ports', 'port -s').replace('includes', 'include -s').replace('restaurants','restaurant -s').replace('kids','kid -s').replace('childs','child -s').replace('prices','price -s').replace('range','range -s').\
                replace('laptops','laptop -s').replace('familys','family -s').replace('specifications','specification -s').replace('ratings','rating -s').replace('products','product -s').\
                    replace('constraints','constraint -s').replace('drives','drive -s').replace('dimensions','dimension -s')
            gen_strs_single.append(gen_str)
            gen_strs_.append(gen_str)                    
            
        gens = gen_strs_
        parallel_corpus.append([gens[:1], gold_strs])
    
    bleuModel   = gentscorer.scoreSBLEU(parallel_corpus)
    print(f'FIELNAME: {target_file}, BLEU: {bleuModel}')


if __name__ == "__main__":
    main()
