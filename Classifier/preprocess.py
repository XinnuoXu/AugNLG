#encoding=utf-8


import numpy
import argparse
import time

from others.logging import init_logger
from prepro import data_builder


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-mode", default='', type=str)
    parser.add_argument("-map_path", default='../../data/')
    parser.add_argument("-raw_path", default='../../line_data')
    parser.add_argument("-save_path", default='../../data/')

    parser.add_argument("-shard_size", default=2000, type=int)
    parser.add_argument('-min_tgt_ntokens', default=3, type=int)
    parser.add_argument('-max_tgt_ntokens', default=50, type=int)

    parser.add_argument("-lower", type=str2bool, nargs='?',const=True,default=True)
    parser.add_argument("-use_bert_basic_tokenizer", type=str2bool, nargs='?',const=True,default=False)

    parser.add_argument('-log_file', default='../logs/cnndm.log')
    parser.add_argument('-dataset', default='')
    parser.add_argument('-n_cpus', default=2, type=int)


    args = parser.parse_args()
    init_logger(args.log_file)
    eval('data_builder.'+args.mode + '(args)')
