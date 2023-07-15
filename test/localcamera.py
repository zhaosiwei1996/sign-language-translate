#!/usr/bin/env python
# coding:utf8
from utils import *
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pickle
import collections
import logging

logger = tf.get_logger()
logger.setLevel(logging.DEBUG)
mp_hands = mp.solutions.hands
draw_util = mp.solutions.drawing_utils
frame_data = collections.deque(maxlen=25)

# 初始化MediaPipe手部识别模型
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# 打开摄像头
cap = cv2.VideoCapture(0)
# 加载训练模型
model = tf.keras.models.load_model('./sign-language-model.h5_1000fit_9994_058')
# 加载pickle文件中的标签
with open('./sign-language-model.pkl', 'rb') as f:
    labels_dict = pickle.load(f)

while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    # 将帧转换为RGB格式
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 检测手部
    hands_results = hands.process(frame_rgb)
    # 提取手部关键点
    if hands_results.multi_hand_landmarks:
        hand_landmarks = hands_results.multi_hand_landmarks[0]
        for hand_landmarks in hands_results.multi_hand_landmarks:
            landmark_list = []
            for landmark in hand_landmarks.landmark:
                landmark_list.append([landmark.x, landmark.y, landmark.z])
                # 在图像上绘制关键点
                draw_util.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                         draw_util.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                         draw_util.DrawingSpec(color=(0, 0, 255), thickness=2))

            landmarks_array = np.array(landmark_list).flatten()
            frame_data.append(landmarks_array)
            # 为了匹配模型输入要求，（None,63,25）加入
            if len(frame_data) == 25:
                model_input = np.array(frame_data).T
                model_input = np.expand_dims(model_input, axis=0)
                # 加载模型并预测
                predictions = model.predict(model_input)
                predicted_class = np.argmax(predictions)
                # 计算百分比
                predicted_prob_percentage = predictions[0][predicted_class] * 100
                # if predicted_prob_percentage < 100:
                #     continue
                # 输出匹配结果
                predicted_label = labels_dict[predicted_class]
                predicted_text = '''word:{},Preprocess:{}'''.format(predicted_label, predicted_prob_percentage)

                print("Predicted_class:{},Predicted_label:{},Preprocess:{}".format(predicted_class, predicted_label,
                                                                                   predicted_prob_percentage))
                # 显示在屏幕上
                cv2.putText(frame, predicted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 显示结果
    cv2.imshow('Hand Gesture Recognition', frame)
    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放摄像头和窗口
cap.release()
cv2.destroyAllWindows()
