#!/usr/bin/env python3
# coding:utf8
from utils import *
import logging
import config

if __name__ == '__main__':
    countlist = []
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    query = mysql_tool.execute_query("desc t_computer;")
    for i in query:
        print(i['Field'] + '\n')
    # query = mysql_tool.select(f"{'t_' + i['gloss']}", "count(*)",
    #                           "videoid={}".format(vid['video_id']))
    # for i in query:
    #     print(i)
    # for word in open('./1.txt'):
    #     # with open(config.worddir, 'r') as f:
    #     # for i in (BaseUtils.string_to_json(f.read())):
    #     #     if i['gloss'] == word.replace('\n', ''):
    #     #         for vid in i['instances']:
    #     words = word.replace('\n', '')
    #     # try:
    #     mysql_tool.connect()
    #     query = mysql_tool.execute_query(
    #         "SELECT COUNT(DISTINCT videoid) as count FROM" + " `" + f"t_{words}`")
    #     # query = mysql_tool.select(f"{'t_' + i['gloss']}", "count(*)",
    #     #                           "videoid={}".format(vid['video_id']))
    #     for i in query:
    #         print(i)

#     except Exception as e:
#         logging.error(e)
#     else:
#         for count in query:
#             for counttwo in count:
#                 # print(counttwo)
#                 countlist.append(counttwo)
#                 logging.info("word:{},count:{}".format(word.replace('\n', ''), counttwo))
#         # if counttwo == 0:
#         #     logging.info(
#         #         "word:{},vid:{},count:{}".format(i['gloss'], vid['video_id'], counttwo))
# # print(list.sort(countlist))
# mysql_tool.close()
