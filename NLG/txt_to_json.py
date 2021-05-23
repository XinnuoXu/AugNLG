#coding=utf8

def rewrite_da(da):
    da_list = da.split()
    intent = da_list[0]
    if intent == 'goodbye':
        return 'goodbye()'
    slots_str = ' '.join(da_list[2:-1])
    if slots_str.strip() == '= ?':
        return '?'+intent+'()'
    slots = slots_str.split(' ; ')
    slot_list = []
    for slot in slots:
        key = slot.split('=')[0].strip()
        if intent == 'request':
            return '?'+intent+'('+key+')'
        value = slot.split('=')[1].strip()
        slot_list.append(key+'='+value)
    if intent in ['select', 'compare', 'confirm']:
        intent = '?'+intent
    return intent + '(' + ';'.join(slot_list) + ')'

def transfer(data_path, dtype):
    json_dict = []
    for line in open(data_path + dtype + '.txt'):
        flist = line.strip().split(' & ')
        text = flist[1].strip()
        da = rewrite_da(flist[0].strip())
        json_obj = []
        json_obj.append(da)
        json_obj.append(text)
        json_obj.append(text)
        json_dict.append(json_obj)
    fpout = open(data_path + dtype + '.json', 'w')
    fpout.write(json.dumps(json_dict))
    fpout.close()

if __name__ == '__main__':
    import sys, os
    import json

    domain = sys.argv[1]
    data_path = 'data/' + domain + '/'

    transfer(data_path, 'train')
    transfer(data_path, 'test')
