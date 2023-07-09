#!/usr/bin/env python3
# coding:utf8
from utils import *
import logging
import config

mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
for word in open('./1-100word.txt'):
    # 提取视频id,生成列表加入线程队列
    with open(config.worddir, 'r') as f:
        for i in (BaseUtils.string_to_json(f.read())):
            if i['gloss'] == word.replace('\n', ''):
                for vid in i['instances']:
                    mysql_tool.connect()
                    try:
                        query = mysql_tool.select("t_{}".format(i['gloss']), "count(*)",
                                                  "videoid={}".format(vid['video_id']))
                    except Exception as e:
                        logging.error(e)
                    else:
                        for count in query:
                            for counttwo in count:
                                if counttwo == 0:
                                    logging.info(
                                        "word:{},vid:{},count:{}".format(i['gloss'], vid['video_id'], counttwo))
mysql_tool.close()
