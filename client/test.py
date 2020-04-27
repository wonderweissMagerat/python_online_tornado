#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#########################################################################
# File Name: test.py
# Author: NLP_zhaozhenyu
# Mail: zhaozhenyu_tx@126.com
# Created Time: 15:28:36 2019-01-25
#########################################################################
import sys
import requests
import json
import time

url_prefix = 'http://0.0.0.0:9111/api/v0/sensitive'

test_file = sys.argv[1]

start = time.time()

for lines in open(test_file):
    data = lines.strip().split('\t')
    docinfo = json.loads(data[1])
    return_info = requests.post(url_prefix,json = docinfo)
    return_dict = json.loads(return_info.text)
    print(str(return_dict['label'])+'\t'+json.dumps(return_dict))

print(time.time()-start)
