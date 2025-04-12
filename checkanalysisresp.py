#!/usr/bin/env python3
# coding:utf8
from utils import *
import logging
import config

if __name__ == '__main__':
    countlist = []
    wordlist = []
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    query = mysql_tool.execute_query("show tables;")
    # analysis word add list
    for wordname in open(config.wordlistfile):
        wordlist.append(wordname)

    for wordname in wordlist:
        with open(config.worddir, 'r') as f:
            for i in (BaseUtils.string_to_json(f.read())):
                if i['gloss'] == wordname.replace('\n', ''):
                    wordnamerep = wordname.replace('\n', '')
                    for vid in i['instances']:
                        sql = "select count(*) from `t_" + wordnamerep + '`' + ''' where ''' + "videoid={}".format(
                            vid['video_id'])
                        logging.info(sql)
                        query = mysql_tool.execute_query(sql)
                        if query:
                            for i in query:
                                if i['count(*)'] == 0:
                                    with open('./error.log', 'a+') as f:
                                        f.write(wordnamerep + ':' + vid['video_id'] + ":" + str(i['count(*)']) + '\n')
                                else:
                                    logging.info(wordnamerep + ':' + vid['video_id'] + ":" + str(i['count(*)']))
                        else:
                            pass
