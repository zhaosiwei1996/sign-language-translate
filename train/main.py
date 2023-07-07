#!/usr/bin/env python3
# coding:utf8
from utils import *
import mediapipe as mp
import cv2

# 初始化MediaPipe的脸部和手部关键点识别模块
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
# 初始化MediaPipe的绘图工具
draw_util = mp.solutions.drawing_utils


def worker():
    # 创建视频播放器
    video_player = cv2.VideoCapture('D:\\signdata\\videos\\01157.mp4')
    # 运行脸部和手部关键点识别
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands, \
            mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face:
        while True:
            # 逐帧读取视频
            ret, frame = video_player.read()
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
                    # print(face_landmarks.landmark)
                    draw_util.draw_landmarks(frame, face_landmarks, mp_face.FACEMESH_CONTOURS,
                                             draw_util.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                                             draw_util.DrawingSpec(color=(0, 0, 255), thickness=1))
            # 绘制手部关键点
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    # print(face_landmarks.landmark)
                    draw_util.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                             draw_util.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                             draw_util.DrawingSpec(color=(0, 0, 255), thickness=2))
            # 显示帧图像
            cv2.imshow('Video', frame)
            # 按下 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if face_results.multi_face_landmarks == None:
                continue
            elif hands_results.multi_hand_landmarks == None:
                continue
            else:
                BaseUtils.append_to_file('./1.txt', str(face_results.multi_face_landmarks))
                BaseUtils.append_to_file('./2.txt', str(hands_results.multi_hand_landmarks))

    # 释放视频播放器和关闭窗口
    video_player.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    worker()
