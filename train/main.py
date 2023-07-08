#!/usr/bin/env python3
# coding:utf8
from utils import *
import mediapipe as mp
import cv2
import multiprocessing
import logging
import os
import config

# 初始化MediaPipe的绘图工具
# draw_util = mp.solutions.drawing_utils
# 手部检测相关
mp_hands = mp.solutions.hands
# 人脸检测相关
mp_face = mp.solutions.face_mesh
# 脸部和手部关键点识别
hands = mp_hands.Hands(static_image_mode=config.static_image_mode, max_num_hands=config.max_num_hands,
                       min_detection_confidence=config.min_detection_confidence)
face = mp_face.FaceMesh(static_image_mode=config.static_image_mode, refine_landmarks=config.refine_landmarks,
                        min_detection_confidence=config.min_detection_confidence,
                        min_tracking_confidence=config.min_tracking_confidence)


def testdef(vidfile):
    logging.info(vidfile.split(',')[0])
    logging.info(vidfile)
    logging.info(vidfile.split(r'\\')[4].split('.mp4')[0])


def worker(vidfile):
    vid = vidfile.split(r'\\')[4].split('.mp4')[0]
    vidword = vidfile.split(',')[0]
    vidfile = vidfile.split(',')[1]
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    logging.info('video:{},开始分析'.format(vidfile))
    # 创建视频播放器
    video_player = cv2.VideoCapture(vidfile)
    # 开始分析计时
    starttime = BaseUtils.get_timestamp()
    while video_player.isOpened():
        # 逐帧读取视频
        ret, frame = video_player.read()
        # # 跳过空帧
        if not ret:
            break
        # 将图像从BGR转换为RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 运行脸部关键点识别
        face_results = face.process(frame_rgb)
        # 运行手部关键点识别
        hands_results = hands.process(frame_rgb)
        # 绘制脸部关键点
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    data = {'videoid': vid, 'face': 1, 'both_hands': 0, 'x_landmark': landmark.x,
                            'y_landmark': landmark.y, 'z_landmark': landmark.z}
                    # logging.info("写入数据:{}".format(data))
                    mysql_tool.insert(vidword, data)
        # 绘制手部关键点
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    data = {'videoid': vid, 'face': 0, 'both_hands': 1, 'x_landmark': landmark.x,
                            'y_landmark': landmark.y, 'z_landmark': landmark.z}
                    # logging.info("写入数据:{}".format(data))
                    mysql_tool.insert(vidword, data)
        # 显示帧图像
        # cv2.imshow('Video', frame)
        # 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    endtime = BaseUtils.get_timestamp()
    logging.info('video:{},分析完成,耗时:{}'.format(vidfile, str(endtime - starttime)))
    # 释放视频播放器和关闭窗口
    video_player.release()
    # cv2.destroyAllWindows()
    mysql_tool.close()


if __name__ == '__main__':
    # 建表
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    # 线程列表
    threadlist = []
    # 并发线程数设置
    pool = multiprocessing.Pool(processes=config.processes)

    # 单循环单词list
    for word in open('./1-100word.txt'):
        # 提取视频id,生成列表加入线程队列
        mysql_tool.connect()
        mysql_tool.create_table('t_{}'.format(word.replace('\n', '')), config.createtablesql)
        mysql_tool.close()
        with open(config.worddir, 'r') as f:
            for i in (BaseUtils.string_to_json(f.read())):
                # if i['gloss'] == config.gloss:
                if i['gloss'] == word.replace('\n', ''):
                    for vid in i['instances']:
                        # videofile = r"t_{},{}{}.mp4".format(config.gloss, config.viddir, vid['video_id'])
                        videofile = r"t_{},{}{}.mp4".format(word.replace('\n', ''), config.viddir, vid['video_id'])
                        # 检查视频文件是否存在,存在添加到existsvidfile list,找不到直接跳过
                        if os.path.exists(videofile.split(',')[1]):
                            logging.info('videofile:{},存在'.format(videofile))
                            threadlist.append(videofile)
                        else:
                            logging.error('videofile:{},不存在'.format(videofile))

    logging.info("found vidfile:{}".format(threadlist))

    # 定义任务列表
    tasks = [i for i in threadlist]
    # 使用map方法并发执行任务
    pool.map(worker, tasks)
    # pool.map(testdef, tasks)
    # 关闭进程池
    pool.close()
    pool.join()
    
