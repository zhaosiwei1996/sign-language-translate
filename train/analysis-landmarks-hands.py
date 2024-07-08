#!/usr/bin/env python3
# coding:utf8
from utils import *
import mediapipe as mp
import cv2
import multiprocessing
import logging
import os
import config

# init mediapipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=config.static_image_mode, max_num_hands=config.max_num_hands,
                       min_detection_confidence=config.min_detection_confidence)


# to mysql save data
def mysqlsave(tablename, alldata):
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    try:
        mysql_tool.insert_many(tablename, alldata)
    except Exception as e:
        logging.error(e)
        logging.error("table:{}".format(tablename))
    mysql_tool.close()


# thread worker
def worker(vidfile):
    alldata = []
    frame_count = 0
    vid = vidfile.split(r'\\')[config.splitnum].split('.mp4')[0]
    vidword = vidfile.split(',')[0]
    vidfile = vidfile.split(',')[1]
    logging.info('video:{},start analysis'.format(vidfile))
    # create video play
    video_player = cv2.VideoCapture(vidfile)
    total_frames = int(video_player.get(cv2.CAP_PROP_FRAME_COUNT))
    # start analysis time
    starttime = BaseUtils.get_timestamp()
    while video_player.isOpened():
        # while True frame
        ret, frame = video_player.read()
        # skip not ret
        if not ret:
            break
        # BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # start hands analysis
        hands_results = hands.process(frame_rgb)
        hand_landmarks = hands_results.multi_hand_landmarks
        # analysis hands xyz
        if hand_landmarks is not None:
            frame_count += 1
            for landmark in hand_landmarks:
                data_points = {}
                for i in range(len(config.hands_nameslist)):
                    # 21 hands xyz analysis add dist
                    data_points.update({
                        'videoid': vid, 'hand_frame_count': frame_count, 'video_total_frames': total_frames,
                        config.hands_nameslist[i] + '_x': landmark.landmark[i].x,
                        config.hands_nameslist[i] + '_y': landmark.landmark[i].y,
                        config.hands_nameslist[i] + '_z': landmark.landmark[i].z,
                    })
                alldata.append(data_points)
        # cv2.imshow('Video', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    # print(alldata)
    # to mysql save
    mysqlsave(vidword, alldata)
    endtime = BaseUtils.get_timestamp()
    logging.info('video:{},done analysis,time-consuming:{}'.format(vidfile, str(endtime - starttime)))
    # break video windows
    cv2.destroyAllWindows()
    video_player.release()


if __name__ == '__main__':
    foundvidfilecount = 0
    notfoundvidfilecount = 0
    # thread list
    threadlist = []
    # threadlist = [r't_hat,F:\\signdata\\WLASL\\videos\\26712.mp4',
    #               r't_hat,F:\\signdata\\WLASL\\videos\\28206.mp4', ]
    # analysis word list
    wordlist = []
    # connect mysql
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    # thread number
    pool = multiprocessing.Pool(processes=config.processes)
    # analysis word add list
    for wordname in open(config.wordlistfile):
        wordlist.append(wordname)
    # create mysql tables
    for wordname in wordlist:
        mysql_tool.connect()
        logging.info("create table:{}".format(wordname.replace('\n', '')))
        mysql_tool.create_table("t_{}".format(wordname.replace('\n', '')), config.createtablesql)
        mysql_tool.close()
    # search files. searchd files to thread list
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

    # for threadlist
    tasks = [i for i in threadlist]
    # start worker
    pool.map(worker, tasks)
    # close thread pool
    pool.close()
    pool.join()
