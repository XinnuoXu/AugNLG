#coding=utf8

import os
import re
import sys
import json
import argparse
import multiprocessing
from nltk import word_tokenize

MIN_LEN = 2
MAX_LEN = 40

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def one_file(path):
    utterances = []
    for line in open(path):
        json_obj = json.loads(line.strip())
        response = json_obj["response"].strip().replace('\n', ' ').replace('\r', ' ')
        toks = response.split()
        if len(toks) < MIN_LEN:
            continue
        if len(toks) > MAX_LEN:
            continue
        utterances.append(response)
    return utterances

def read_raw_data(base_path, output_path, thread_num=28):

    path_list = []
    pool = multiprocessing.Pool(processes=thread_num)
    fpout = open(output_path, 'w')
    utt_num = 0

    for filename in os.listdir(base_path):
        if not filename.startswith('train-'):
            continue
        if len(path_list) == thread_num:
            utterances = pool.map(one_file, path_list)
            for utts in utterances:
                utt_num += len(utts)
                fpout.write('\n'.join(utts) + '\n')
            print ('Processed', utt_num, 'utterances...')
            del path_list[:]
        path_list.append(os.path.join(base_path, filename))

    if len(path_list) > 0:
        utterances = pool.map(one_file, path_list)
        for utts in utterances:
            utt_num += len(utts)
            fpout.write('\n'.join(utts) + '\n')

    print ('Number of utterances:', utt_num)
    fpout.close()

def preprocess_number(string):
    replace_num=True
    tokenization=True
    lower = True
    raw_string = string
    if tokenization:
        string = ' '.join(word_tokenize(string))
    if lower:
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
    return string.replace('[NUMBER]', '11111'), raw_string

def delexicalize_number(input_path, output_path, thread_num=28):

    pool = multiprocessing.Pool(processes=thread_num)
    fpout = open(output_path, 'w')
    utt_list = []

    for line in open(input_path):
        if len(utt_list) == thread_num:
            utterances = pool.map(preprocess_number, utt_list)
            for utts in utterances:
                fpout.write(utts[0] + '\t' + utts[1] + '\n')
            del utt_list[:]
        utt_list.append(line.strip())

    if len(utt_list) > 0:
        utterances = pool.map(preprocess_number, utt_list)
        for utts in utterances:
            fpout.write(utts[0] + '\t' + utts[1] + '\n')

    fpout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", default='read_raw', type=str, choices=['read_raw', 'delexicalization'])
    parser.add_argument("-min_length", default=2, type=int)
    parser.add_argument("-max_length", default=40, type=int)
    parser.add_argument("-base_path", default='/scratch/xxu/reddit/')
    parser.add_argument("-utterance_path", default='/scratch/xxu/reddit.utterances')
    parser.add_argument("-delex_path", default='/scratch/xxu/reddit.delex')
    parser.add_argument("-thread_num", default=20, type=int)
    args = parser.parse_args()

    MIN_LEN = args.min_length
    MAX_LEN = args.max_length

    if args.mode == 'read_raw':
        read_raw_data(args.base_path, args.utterance_path, args.thread_num)
    if args.mode == 'delexicalization':
        delexicalize_number(args.utterance_path, args.delex_path, args.thread_num)

