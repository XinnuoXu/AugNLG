#coding=utf8

def transfer(data_path, dtype):
    json_dict = []
    for line in open(data_path + dtype + '.txt'):
        flist = line.strip().split(' & ')
        text = flist[1]
        da = flist[0]
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
