import gc
import glob
import hashlib
import itertools
import json
import os
import random
import re
import copy
import subprocess
from collections import Counter
from os.path import join as pjoin

import torch
from multiprocessing import Pool

from others.logging import logger
from others.tokenization import BertTokenizer


class BertData():
    def __init__(self, args):
        self.args = args
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

        self.sep_token = '[SEP]'
        self.cls_token = '[CLS]'
        self.pad_token = '[PAD]'
        self.sep_vid = self.tokenizer.vocab[self.sep_token]
        self.cls_vid = self.tokenizer.vocab[self.cls_token]
        self.pad_vid = self.tokenizer.vocab[self.pad_token]


    def preprocess(self, src, use_bert_basic_tokenizer=False):

        src_tokens = src.strip().split()
        if len(src_tokens) > self.args.max_tgt_ntokens or len(src_tokens) < self.args.min_tgt_ntokens:
            return None

        src_subtokens = self.tokenizer.tokenize(src)
        src_subtokens = [self.cls_token] + src_subtokens

        src_subtoken_idxs = self.tokenizer.convert_tokens_to_ids(src_subtokens)

        return src_subtoken_idxs


def format_to_bert(args):
    if (args.dataset != ''):
        datasets = [args.dataset]
    else:
        datasets = ['train', 'test', 'dev']
    for corpus_type in datasets:
        a_lst = []
        for json_f in glob.glob(pjoin(args.raw_path, '*' + corpus_type + '.*.json')):
            real_name = json_f.split('/')[-1]
            a_lst.append((corpus_type, json_f, args, pjoin(args.save_path, real_name.replace('json', 'bert.pt'))))
        print(a_lst)
        pool = Pool(args.n_cpus)
        for d in pool.imap(_format_to_bert, a_lst):
            pass
        pool.close()
        pool.join()


def _format_to_bert(params):
    corpus_type, json_file, args, save_file = params

    if (os.path.exists(save_file)):
        logger.info('Ignore %s' % save_file)
        return

    bert = BertData(args)

    logger.info('Processing %s' % json_file)
    jobs = json.load(open(json_file))
    datasets = []
    for d in jobs:
        raw_source, label = d['src'], d['label']
        if (args.lower):
            source = raw_source.lower()
        src_subtoken_idxs = bert.preprocess(source, args.use_bert_basic_tokenizer)

        if (src_subtoken_idxs is None):
            continue

        b_data_dict = {"src": src_subtoken_idxs, 'clss': label, 'src_txt': raw_source}
        datasets.append(b_data_dict)

    logger.info('Processed instances %d' % len(datasets))
    logger.info('Saving to %s' % save_file)
    torch.save(datasets, save_file)
    datasets = []
    gc.collect()


def format_text_to_json(args):
    if (args.dataset != ''):
        datasets = [args.dataset]
    else:
        datasets = ['train', 'test', 'dev']

    for corpus_type in datasets:
        root_src = args.raw_path + corpus_type + ".txt"

        srcs = []
        for line in open(root_src):
            flist = line.strip().split('\t')
            if len(flist) != 2:
                continue
            src = flist[0]
            label = int(flist[1])
            srcs.append((src, label))

        json_objs = []
        for i, src in enumerate(srcs):
            json_objs.append({'src': src[0], 'label': src[1]})

        dataset = []; p_ct = 0
        for d in json_objs:
            dataset.append(d)
            if (len(dataset) > args.shard_size):
                pt_file = "{:s}.{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
                with open(pt_file, 'w') as save:
                    save.write(json.dumps(dataset))
                    p_ct += 1
                    dataset = []

        if (len(dataset) > 0):
            pt_file = "{:s}.{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
            with open(pt_file, 'w') as save:
                save.write(json.dumps(dataset))
                p_ct += 1
                dataset = []
