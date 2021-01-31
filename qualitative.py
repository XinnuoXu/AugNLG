#coding=utf8

import sys
import json
import os
models = ['GPT-2', 'SC-GPT', 'AUG-GPT', 'AUG-GPT-SC']

def load_one_model(model):
    log_obj = {}
    path = 'tmp.log.bleu.'+model
    with open(path, encoding="utf-8") as f:
        json_obj = json.loads(f.read().strip())
        for item in json_obj:
            if len(item) == 5:
                log_obj[item[0]] = {'ref':item[2], 'pred':item[1], 'bleu':item[3], 'err':item[4]}
            else:
                log_obj[item[0]] = {'ref':item[2], 'pred':item[1], 'bleu':item[3]}
    return log_obj

def err_better(models_obj):
    examples = []
    for mr in models_obj['GPT-2']:
        if models_obj['GPT-2'][mr]['err'] <= models_obj['AUG-GPT'][mr]['err']:
            continue
        if models_obj['SC-GPT'][mr]['err'] <= models_obj['AUG-GPT-SC'][mr]['err']:
            continue
        output = [mr, models_obj['GPT-2'][mr]['ref']]
        for model in models:
            output.append(models_obj[model][mr]['pred'])
        examples.append(output)
    return examples

def bleu_better(models_obj):
    examples = []
    for mr in models_obj['GPT-2']:
        if sum(models_obj['GPT-2'][mr]['bleu']) >= sum(models_obj['AUG-GPT'][mr]['bleu']):
            continue
        if sum(models_obj['SC-GPT'][mr]['bleu']) >= sum(models_obj['AUG-GPT-SC'][mr]['bleu']):
            continue
        output = [mr, models_obj['GPT-2'][mr]['ref']]
        for model in models:
            output.append(models_obj[model][mr]['pred'])
        examples.append(output)
    return examples

def both_better(models_obj):
    examples = []
    for mr in models_obj['GPT-2']:
        if models_obj['GPT-2'][mr]['err'] <= models_obj['AUG-GPT'][mr]['err']:
            continue
        if models_obj['SC-GPT'][mr]['err'] <= models_obj['AUG-GPT-SC'][mr]['err']:
            continue
        if sum(models_obj['GPT-2'][mr]['bleu']) >= sum(models_obj['AUG-GPT'][mr]['bleu']):
            continue
        if sum(models_obj['SC-GPT'][mr]['bleu']) >= sum(models_obj['AUG-GPT-SC'][mr]['bleu']):
            continue
        output = [mr, models_obj['GPT-2'][mr]['ref']]
        for model in models:
            output.append(models_obj[model][mr]['pred'])
        examples.append(output)
    return examples

if __name__ == '__main__':
    models_obj = {}
    for model in models:
        log_obj = load_one_model(model)
        models_obj[model] = log_obj
    if sys.argv[1] == 'bleu_better':
        examples = bleu_better(models_obj)
        for ex in examples:
            print (ex[0])
            print (ex[1])
            for i, model in enumerate(models):
                print (model + '\t' + ex[2+i])
            print ('')
    if sys.argv[1] == 'err_better':
        examples = err_better(models_obj)
        for ex in examples:
            print (ex[0])
            print (ex[1])
            for i, model in enumerate(models):
                print (model + '\t' + ex[2+i])
            print ('')
    if sys.argv[1] == 'both_better':
        examples = both_better(models_obj)
        for ex in examples:
            print (ex[0])
            print (ex[1])
            for i, model in enumerate(models):
                print (model + '\t' + ex[2+i])
            print ('')
