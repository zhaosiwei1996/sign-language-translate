#!/usr/bin/env python3
# coding:utf8
from utils import *

with open('./WLASL_v0.3.json', 'r') as f:
    for i in (BaseUtils.string_to_json(f.read())):
        # print(i['gloss'])
        BaseUtils.append_to_file('./3.txt', i['gloss'] + '\n')
        # if i['gloss'] == 'book':
        #     for b in i['instances']:
        #         print(b['video_id'])
        # else:
        #     break
