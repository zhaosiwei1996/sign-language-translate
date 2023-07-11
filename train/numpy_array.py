#!/usr/bin/env python
# coding:utf8
from utils import *
import numpy as np
import config
import logging

if __name__ == '__main__':
    # 转换numarray数组list
    landmarks = []
    # 循环内extend list
    single_frame_landmarks = []
    # 100个单词list
    # wordlist = ['accident', 'africa', 'all', 'apple', 'basketball', 'bed', 'before', 'bird', 'birthday', 'black',
    #             'blue', 'book', 'bowling', 'brown', 'but', 'can', 'candy', 'chair', 'change', 'cheat', 'city',
    #             'clothes', 'color', 'computer', 'cook', 'cool', 'corn', 'cousin', 'cow', 'dance', 'dark', 'deaf',
    #             'decide', 'doctor', 'dog', 'drink', 'eat', 'enjoy', 'family', 'fine', 'finish', 'fish', 'forget',
    #             'full', 'give', 'go', 'graduate', 'hat', 'hearing', 'help', 'hot', 'how', 'jacket', 'kiss', 'language',
    #             'last', 'later', 'letter', 'like', 'man', 'many', 'medicine', 'meet', 'mother', 'need', 'no', 'now',
    #             'orange', 'paint', 'paper', 'pink', 'pizza', 'play', 'pull', 'purple', 'right', 'same', 'school',
    #             'secretary', 'shirt', 'short', 'son', 'study', 'table', 'tall', 'tell', 'thanksgiving', 'thin',
    #             'thursday', 'time', 'walk', 'want', 'what', 'white', 'who', 'woman', 'work', 'wrong', 'year', 'yes']
    wordlist = ['book', 'computer', 'drink', 'go']
    # 数据库连接
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    # 遍历数据库,xyz数据提取出来
    queryselect = mysql_tool.select("t_go", "x_landmark,y_landmark,z_landmark", "both_hands=1")
    for resp1 in queryselect:
        landmarks.append(list(resp1))
    mysql_tool.close()
    print(landmarks)
    # print(np.array(landmarks))
    # np.save('./go.npy', np.array(landmarks))
