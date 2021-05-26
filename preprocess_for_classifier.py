#coding=utf8

import sys, os
import random
from key_ngrams import preprocess
from nltk import word_tokenize

def random_sample(in_domain_exps, aug_data, out_domain_path, out_domain_example_num, ratio=10):
    out_domain_sample_num = len(in_domain_exps) * ratio
    START_IDX = random.randint(0, out_domain_example_num-out_domain_sample_num)
    out_domain_exps = []
    for i, line in enumerate(open(out_domain_path)):
        if i < START_IDX:
            continue
        if len(out_domain_exps) >= out_domain_sample_num:
            break
        utt = line.strip().split('\t')[0]
        if utt not in aug_data:
            out_domain_exps.append(utt)
    return out_domain_exps


def read_from_aug(process_domain, retrive_path):
    aug_data = set()
    aug_path = retrive_path.replace('[DOMAIN]', process_domain)
    for filename in os.listdir(aug_path):
        for line in open(aug_path + '/' + filename):
            flist = line.strip().split('\t')
            if len(flist) != 2:
                continue
            utt = flist[0]
            aug_data.add(utt)
    return aug_data


def get_fewshot_in_domain(in_domain_path, process_domain):
    in_domain_exps = []
    in_domain_path = in_domain_path.replace('[DOMAIN]', process_domain)
    for line in open(in_domain_path):
        flist = line.strip().split(' & ')
        if len(flist) != 2:
            continue
        utterance = flist[1].strip()
        utterance = preprocess(utterance, tokenization=False)
        in_domain_exps.append(utterance)
    return in_domain_exps


def write_out(process_domain, 
                in_domain_exps, 
                out_domain_exps, 
                aug_data, 
                output_dir,
                in_domain_devs=None, 
                out_domain_devs=None):

    # Make output dir
    output_dir = output_dir.replace('[DOMAIN]', process_domain)
    if not os.path.exists(output_dir):
        os.system('mkdir ' + output_dir)

    # Get training data
    fpout = open(output_dir + '/train.txt', 'w')
    utt_list = []
    for utt in in_domain_exps:
        utt_list.append(utt + '\t1')
    for utt in out_domain_exps:
        utt_list.append(utt + '\t0')
    random.shuffle(utt_list)
    for utt in utt_list:
        fpout.write(utt + '\n')
    fpout.close()

    # Get dev data
    if (in_domain_devs is not None) and (out_domain_devs is not None):
        fpout = open(output_dir + '/dev.txt', 'w')
        utt_list = []
        for utt in in_domain_devs:
            utt_list.append(utt + '\t1')
        for utt in out_domain_devs:
            utt_list.append(utt + '\t0')
        random.shuffle(utt_list)
        for utt in utt_list:
            fpout.write(utt + '\n')
        fpout.close()

    # Get testing data
    fpout = open(output_dir + '/test.txt', 'w')
    for utt in aug_data:
        fpout.write(utt + '\t0\n')
    fpout.close()


def initial_train(args):
    process_domain = args.domain

    # Get augment data (test)
    aug_data = read_from_aug(process_domain, args.retrive_path)

    # Get in domain examples (train)
    in_domain_train_path = '%s/train.txt' % args.in_domain_path
    in_domain_exps = get_fewshot_in_domain(in_domain_train_path, process_domain)
    # Get randomly sampled out of domain examples (train)
    out_domain_exps = random_sample(in_domain_exps, aug_data, args.delex_path, 
                                        args.out_domain_example_num, ratio=args.neg_pos_ratio_init)

    # Get in domain examples (test)
    in_domain_test_path = '%s/test.txt' % args.in_domain_path
    in_domain_devs = get_fewshot_in_domain(in_domain_test_path, process_domain)
    # Get randomly sampled out of domain examples (test)
    out_domain_devs = random_sample(in_domain_devs, aug_data, args.delex_path, 
                                        args.out_domain_example_num, ratio=args.neg_pos_ratio_init)
    
    # Write out
    write_out(process_domain, in_domain_exps, out_domain_exps, aug_data, 
                    args.self_learning_path, in_domain_devs, out_domain_devs)


def self_training(args):

    def filter_by_kw(stop_kw, string):
        if not args.use_black_ngrams:
            return True
        for kw in stop_kw:
            if string.find(kw) > -1:
                return False
        return True

    def load_stop_kw(process_domain):
        stop_kw = []
        aug_path = args.retrive_path.replace('[DOMAIN]', process_domain)
        for filename in os.listdir(aug_path):
            key = filename.replace('.txt', '').replace('_', ' ')
            if len([line for line in open(aug_path + '/' + filename)]) >= 10000:
                stop_kw.append(key)
        print (stop_kw)
        return stop_kw

    process_domain = args.domain

    # Get augment data (test)
    aug_data = read_from_aug(process_domain)

    # Get stop kys
    stop_kw = load_stop_kw(process_domain)
    # Get in domain examples (train)
    in_domain_train_path = '%s/train.txt' % args.in_domain_path
    in_domain_exps = get_fewshot_in_domain(in_domain_train_path, process_domain)
    out_domain_exps = []
    # Get augmented positive/negtive data (train)
    prediction_path = "%s/prediction.txt" % args.self_learning_path
    prediction_path = PREDICTION_PATH.replace('[DOMAIN]', process_domain)
    for line in open(prediction_path):
        flist = line.strip().split('\t')
        score = float(flist[0])
        if score > args.pos_cls_threshold and filter_by_kw(stop_kw, flist[1]):
            in_domain_exps.append(flist[1])
        if score < args.neg_cls_threshold:
            out_domain_exps.append(flist[1])
    neg_sample_num = args.neg_pos_ratio * len(in_domain_exps)
    if len(out_domain_exps) > neg_sample_num:
        out_domain_exps = random.sample(out_domain_exps, neg_sample_num)

    # Write out
    write_out(process_domain, in_domain_exps, out_domain_exps, aug_data)
    return len(in_domain_exps)


