#coding=utf8

import sys, os
import argparse
from preprocess_for_classifier import initial_train, self_training

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
    parser.add_argument("-delex_path", default='./reddit.delex', type=str)
    parser.add_argument("-retrive_path", default='./augmented_data/[DOMAIN].aug/', type=str)
    parser.add_argument("-self_learning_path", default='./augmented_data/[DOMAIN].cls/', type=str)
    parser.add_argument("-in_domain_path", default='./domains/[DOMAIN]/', type=str)
    parser.add_argument("-tmp_training_path", default='./tmp/', type=str)
    parser.add_argument("-min_increment", default=100, type=int)
    parser.add_argument("-max_round", default=10, type=int)
    parser.add_argument("-use_black_ngrams", default=False, type=bool)
    #parser.add_argument("-out_domain_example_num", default=636486504, type=int)
    parser.add_argument("-out_domain_example_num", default=60000, type=int)
    parser.add_argument("-neg_pos_ratio_init", default=10, type=int)
    parser.add_argument("-neg_pos_ratio", default=10, type=int)
    parser.add_argument("-pos_cls_threshold", default=0.99, type=float)
    parser.add_argument("-neg_cls_threshold", default=0.5, type=float)
    args = parser.parse_args()

    initial_train(args)
    os.system('mkdir %s' % args.tmp_training_path)
    train_path = '%s/%s' % (args.tmp_training_path, args.domain)
    target_path = args.self_learning_path.replace('[DOMAIN]', args.domain)
    command = 'cd ./Classifier; sh initial_train.sh ../%s ../%s; cd ../;' % (target_path, train_path)
    os.system(command)

    '''
    last_pos_num = 0
    for iteration in range(1, args.max_round+1):
        pos_num = self_training(args)
        if pos_num - last_pos_num < args.min_increment:
            print ('Iteration finished in round:', iteration)
            break
        last_pos_num = pos_num
        os.system('cd ./Classifier; sh self_learning.sh '+args.domain+' '+str(iteration)+';cd ../;')

    '''
