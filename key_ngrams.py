#coding=utf8

import re
import os
import sys
import random
import argparse
from nltk import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
    

def preprocess(string, replace_num=True, tokenization=True):
    if tokenization:
        string = ' '.join(word_tokenize(string))
    string = string.lower()
    if replace_num:
        numbers = re.findall(r"\d+\.?\d*",string)
        number_length_dict = {}
        for item in numbers:
            if len(item) not in number_length_dict:
                number_length_dict[len(item)] = []
            number_length_dict[len(item)].append(item)
        for num_len in sorted(number_length_dict.items(), key = lambda d:d[0], reverse = True):
            for number in num_len[1]:
                string = string.replace(number, '[NUMBER]')
    # replace is for tfidf tool
    return string.replace('[NUMBER]', '11111')

def ngram_validation_check(ngram):
    for tok in ngram:
        if len(tok) <= 1:
            return False
    return True

def get_ngrams(string, n):
    ngrams = []
    flist = string.split()
    for i in range(0, len(flist)-n+1):
        if not ngram_validation_check(flist[i:i+n]):
            continue
        ngram = ' '.join(flist[i:i+n])
        ngrams.append(ngram)
    return ngrams

def stopword_filtered(stopwords, key):
    for tok in key.split():
        if tok not in stopwords:
            return False
    return True

if __name__ == '__main__':

    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument("-domain", default='restaurant', type=str)
    parser.add_argument("-in_domain_path", default='./domains/[DOMAIN]/train.txt', type=str)
    parser.add_argument("-delex_path", default='./reddit.delex', type=str)
    parser.add_argument("-keyword_path", default='./augmented_data/[DOMAIN]_system.kws', type=str)
    parser.add_argument("-out_domain_example_num", default=636486504, type=int)
    parser.add_argument("-out_domain_sample_num", default=50000, type=int)
    parser.add_argument("-ngrams", default=2, type=int)
    # filtering thresholds
    parser.add_argument("-in_out_ratio", default=0.1, type=float)
    parser.add_argument("-min_count", default=1, type=int)
    parser.add_argument("-min_tf_idf", default=0.01, type=float)
    args = parser.parse_args()

    in_domain_path = args.in_domain_path
    delex_path = args.delex_path
    keyword_path = args.keyword_path
    out_domain_example_num = args.out_domain_example_num
    out_domain_sample_num = args.out_domain_sample_num

    # Get randomly sampled out of domain examples
    sample_ids = [random.randint(0, out_domain_example_num) for i in range(0, out_domain_sample_num)]
    out_domain_exps = []
    for i, line in enumerate(open(delex_path)):
        #if i in sample_ids:
        #    out_domain_exps.append(line.strip())
        if i >= out_domain_sample_num:
            break
        out_domain_exps.append(line.strip())


    # Get in domain examples
    in_domain_exps = []
    in_domain_path = in_domain_path.replace('[DOMAIN]', args.domain)
    for line in open(in_domain_path):
        flist = line.strip().split(' & ')
        if len(flist) != 2:
            continue
        utterance = flist[1].strip()
        in_domain_exps.append(utterance)


    # In-domain examples
    in_domain_exps = [preprocess(string, tokenization=False) for string in in_domain_exps]
    in_domain_corpus = ' '.join(in_domain_exps)
    # Ngram extraction
    in_domain_ngrams = []
    for string in in_domain_exps:
        in_domain_ngrams += get_ngrams(string, args.ngrams)
    in_count = Counter(in_domain_ngrams)


    # Out-domain utterances
    #out_domain_exps = [preprocess(string) for string in out_domain_exps]
    output_domain_corpus = ' '.join(out_domain_exps)


    # Get tf-idf
    corpus = [in_domain_corpus, output_domain_corpus]
    vocabulary = {}
    for key in in_count:
        vocabulary[key] = len(vocabulary)
    vectorizer = TfidfVectorizer(vocabulary=vocabulary, smooth_idf=True, use_idf=True, ngram_range=(2, 2))
    #vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True, ngram_range=(2, 2))


    # Read result
    tfidf = vectorizer.fit_transform(corpus)
    tfidf_tokens = vectorizer.get_feature_names()
    df_tfidfvect = pd.DataFrame(data = tfidf.toarray(), index = ['In_domain', 'Out_domain'], columns = tfidf_tokens).to_dict()
    #in_domain_sorted = df_tfidfvect[:1].sort_values(by=['In_domain'], axis=1).to_dict()


    # First filtering
    new_dict = {}; stop_words = set()
    print ('Filted phrases: ')
    for key in df_tfidfvect:
        tf_idf = df_tfidfvect[key]['In_domain']
        #print (key, tf_idf, df_tfidfvect[key]['Out_domain'], in_count[key])
        if tf_idf * args.in_out_ratio < df_tfidfvect[key]['Out_domain']:
            print (key, tf_idf, df_tfidfvect[key]['Out_domain'], in_count[key])
            for tok in key.split():
                stop_words.add(tok)
            continue
        if in_count[key] >= args.min_count and tf_idf >= args.min_tf_idf:
            new_dict[key] = tf_idf


    # Second filtering
    filtered_ngrams = {}
    for key in new_dict:
        if stopword_filtered(stop_words, key):
            continue
        filtered_ngrams[key] = new_dict[key]

    # Write out
    fpout = open(keyword_path.replace('[DOMAIN]', args.domain), 'w')
    for item in sorted(filtered_ngrams.items(), key = lambda d:d[1], reverse=True):
        fpout.write(item[0] + '\n')
    fpout.close()
