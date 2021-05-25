#coding=utf8

import sys, os
import argparse
import multiprocessing

REDDIT_PATH = ''
OUTPUT_DIR = ''

def grep(kws):
    k = '_'.join(kws.split())
    command = 'grep \"' + kws + '\" ' + REDDIT_PATH + ' > ' + OUTPUT_DIR + k + '.txt'
    os.system(command)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-domain", default='restaurant', type=str)
    parser.add_argument("-delex_path", default='./reddit.delex', type=str)
    parser.add_argument("-keyword_path_pattern", default='./augmented_data/[DOMAIN]_system.kws', type=str)
    parser.add_argument("-retrieve_path_pattern", default='./augmented_data/[DOMAIN].aug/', type=str)
    parser.add_argument("-thread_num", default=20, type=int)
    args = parser.parse_args()

    REDDIT_PATH = args.delex_path
    OUTPUT_DIR = args.retrieve_path_pattern.replace('[DOMAIN]', args.domain)
    if not os.path.exists(OUTPUT_DIR):
        os.system('mkdir ' + OUTPUT_DIR)
    input_path = args.keyword_path_pattern.replace('[DOMAIN]', args.domain)

    pool = multiprocessing.Pool(processes=args.thread_num)
    kws_list = []

    for line in open(input_path):
        if len(kws_list) == args.thread_num:
            utterances = pool.map(grep, kws_list)
            del kws_list[:]
        kws_list.append(line.strip())

    if len(kws_list) > 0:
        utterances = pool.map(grep, kws_list)

