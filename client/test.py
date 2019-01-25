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

url_prefix = 'localhost:9003/api/v0'

test_file = 'data'

start = time.time()

for lines in open(test_file):
    data = lines.strip().split('\t')
    docid = data[0]
    docinfo = {'docid':docid}
    return_info = requests.port(url_prefix,json = docinfo)
    return_dict = json.loads(return_info)
    print(return_dict)

print(time.time()-start)
