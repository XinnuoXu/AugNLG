#coding=utf8

import sys
import os
import json
import numpy as np

dec_path = 'result_[DOMAIN].[ITT]/results_[DOMAIN]_[D_NUM].json'
target_path = './results_[DOMAIN]_[D_NUM].json'

org_test_path = 'data_moredata.[ITT]/sgd.[D_NUM]/[DOMAIN]/test.txt'
test_path = './data/[DOMAIN]_[D_NUM]/test.txt'

d_nums = ['50', '100', '200', '500', '1500']
itts = ['1', '2', '3', '4', '5']
domains = ['sgd_buses', 'sgd_flights', 'sgd_movies', 'sgd_ridesharing']

if __name__ == '__main__':
    obj = {}
    for domain in domains:
        means = []; stds = []
        for d_num in d_nums:
            scores = []
            for itt in itts:
                decode_file = dec_path.replace('[DOMAIN]', domain).replace('[ITT]', itt).replace('[D_NUM]', d_num)
                target_file = target_path.replace('[DOMAIN]', domain).replace('[D_NUM]', d_num)
                os.system('cp '+decode_file+' '+target_file)

                org_test_file = org_test_path.replace('[DOMAIN]', domain).replace('[ITT]', itt).replace('[D_NUM]', d_num)
                test_file = test_path.replace('[DOMAIN]', domain).replace('[D_NUM]', d_num)
                os.system('cp '+org_test_file+' '+test_file)

                os.system('sh evaluate_bleu.sh '+domain+'_'+d_num+' > tmp.res')
                with open('tmp.res', encoding="utf-8") as f:
                    text = f.read().strip()
                    scores.append(float(text.split()[-1]))
            scores = np.array(scores) * 100
            mean = np.mean(scores)
            std = np.std(scores)
            means.append(mean)
            stds.append(std)
        obj[domain] = (means, stds)
    print (json.dumps(obj))
