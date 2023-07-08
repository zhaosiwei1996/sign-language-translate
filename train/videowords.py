#!/usr/bin/env python3
# coding:utf8
from utils import *

videolist = []
with open('./info.json', 'r') as f:
    for i in (BaseUtils.string_to_json(f.read())):
        # print(i['gloss'])
        BaseUtils.append_to_file('allword.txt', i['gloss'] + '\n')
        # if i['gloss'] == 'book':
        #     for b in i['instances']:
        #         videolist.append(b['video_id'])
    # print(videolist)
