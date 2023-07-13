#!/usr/bin/env python3
# coding:utf8
from utils import *
import mediapipe as mp
import cv2
import multiprocessing
import logging
import os
import config
import sys

# 手部检测相关
mp_hands = mp.solutions.hands
# 脸部和手部关键点识别
hands = mp_hands.Hands(static_image_mode=config.static_image_mode, max_num_hands=config.max_num_hands,
                       min_detection_confidence=config.min_detection_confidence)


def mysqlsave(tablename, alldata):
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    try:
        mysql_tool.insert_many(tablename, alldata)
    except Exception as e:
        logging.error(e)
        logging.error("table:{}".format(tablename))
    mysql_tool.close()


def worker(vidfile):
    alldata = []
    data_points = {}
    vid = vidfile.split(r'\\')[config.splitnum].split('.mp4')[0]
    vidword = vidfile.split(',')[0]
    vidfile = vidfile.split(',')[1]
    logging.info('video:{},start analysis'.format(vidfile))
    # 创建视频播放器
    video_player = cv2.VideoCapture(vidfile)
    total_frames = int(video_player.get(cv2.CAP_PROP_FRAME_COUNT))
    # 开始分析计时
    starttime = BaseUtils.get_timestamp()
    while video_player.isOpened():
        # 逐帧读取视频
        ret, frame = video_player.read()
        # 跳过空帧
        if not ret:
            break
        # 将图像从BGR转换为RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 运行手部关键点识别
        hands_results = hands.process(frame_rgb)
        hand_landmarks = hands_results.multi_hand_landmarks
        # 提取手部关键点
        if hand_landmarks is not None:
            for landmark in hand_landmarks:
                for i in range(len(config.hands_nameslist)):
                    data_points.update({
                        'videoid': vid, 'video_total_frames': total_frames, 'face': 0, 'both_hands': 1,
                        config.hands_nameslist[i] + '_x': landmark.landmark[i].x,
                        config.hands_nameslist[i] + '_y': landmark.landmark[i].y,
                        config.hands_nameslist[i] + '_z': landmark.landmark[i].z,
                    })
                    alldata.append(data_points)
            # 显示帧图像
            # cv2.imshow('Video', frame)
            # 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # 数据保存
    # print(alldata)
    mysqlsave(vidword, alldata)
    endtime = BaseUtils.get_timestamp()
    logging.info('video:{},done analysis,time-consuming:{}'.format(vidfile, str(endtime - starttime)))
    # 释放视频播放器和关闭窗口
    video_player.release()


if __name__ == '__main__':
    foundvidfilecount = 0
    notfoundvidfilecount = 0
    # 线程列表
    threadlist = []
    # threadlist = [r't_hat,F:\\signdata\\WLASL\\videos\\26712.mp4',
    #               r't_hat,F:\\signdata\\WLASL\\videos\\28206.mp4', ]
    # 需要分析的单词list
    wordlist = []
    # 连接数据库
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    # 并发线程数设置
    pool = multiprocessing.Pool(processes=config.processes)
    # # 单循环单词list
    for wordname in open(config.wordlistfile):
        wordlist.append(wordname)
    # 建表
    for wordname in wordlist:
        mysql_tool.connect()
        logging.info("create table:{}".format(wordname.replace('\n', '')))
        mysql_tool.create_table("t_{}".format(wordname.replace('\n', '')), config.createtablesql)
        mysql_tool.close()
    # 查找对应的数据集是否存在
    for wordname in wordlist:
        with open(config.worddir, 'r') as f:
            for i in (BaseUtils.string_to_json(f.read())):
                if i['gloss'] == wordname.replace('\n', ''):
                    for vid in i['instances']:
                        videofile = r"t_{},{}{}.mp4".format(wordname.replace('\n', ''), config.viddir, vid['video_id'])
                        # 检查视频文件是否存在,存在添加到线程列表,找不到直接跳过
                        if os.path.exists(videofile.split(',')[1]):
                            logging.info('videofile:{},found'.format(videofile))
                            threadlist.append(videofile)
                            foundvidfilecount += 1
                        else:
                            logging.error('videofile:{},not found'.format(videofile))
                            notfoundvidfilecount += 1

    logging.info("found vidfile count:{}".format(foundvidfilecount))
    logging.info("not found vidfile count:{}".format(notfoundvidfilecount))

    # 定义任务列表
    tasks = [i for i in threadlist]
    # 使用map方法并发执行任务
    pool.map(worker, tasks)
    # 关闭进程池
    pool.close()
    pool.join()
