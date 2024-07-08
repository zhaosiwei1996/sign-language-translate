#!/usr/bin/env python
# coding:utf8
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pickle
import collections
import logging
from utils import *
import config

logger = tf.get_logger()
logger.setLevel(logging.DEBUG)

# 初始化MediaPipe hands
mp_hands = mp.solutions.hands
draw_util = mp.solutions.drawing_utils
frame_data = collections.deque(maxlen=25)

# 加载模型和标签
def load_model_and_labels(model_path, label_path):
    model = tf.keras.models.load_model(model_path)
    with open(label_path, 'rb') as f:
        labels_dict = pickle.load(f)
    return model, labels_dict

# 绘制手部关节点和连接线
def draw_hand_landmarks(frame, hand_landmarks, mp_hands, draw_util):
    # 定义关节点索引的颜色和大小
    index_color = (255, 255, 255)  # 白色
    index_font_scale = 0.5
    index_thickness = 1

    # 定义关节点连接线的颜色和样式
    connection_color = (0, 255, 0)  # 绿色
    connection_thickness = 2

    # 绘制关节点连接线
    draw_util.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                             draw_util.DrawingSpec(color=connection_color, thickness=connection_thickness, circle_radius=4),
                             draw_util.DrawingSpec(color=(0, 0, 255), thickness=2))

    # 获取帧的尺寸
    h, w, _ = frame.shape

    # 绘制每个关节点的索引
    for idx, landmark in enumerate(hand_landmarks.landmark):
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, index_font_scale, index_color, index_thickness)

    return frame

# 处理每帧
def process_frame(frame, hands, draw_util, frame_data, model, labels_dict):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hands_results = hands.process(frame_rgb)

    if hands_results.multi_hand_landmarks:
        for hand_landmarks in hands_results.multi_hand_landmarks:
            landmark_list = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
            landmarks_array = np.array(landmark_list).flatten()
            frame_data.append(landmarks_array)
            if len(frame_data) == 25:
                model_input = np.expand_dims(np.array(frame_data).T, axis=0)
                predictions = model.predict(model_input)
                predicted_class = np.argmax(predictions)
                predicted_label = labels_dict[predicted_class]
                cv2.putText(frame, predicted_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 绘制手部关节点和索引
            frame = draw_hand_landmarks(frame, hand_landmarks, mp_hands, draw_util)

    return frame

# 主函数
def main():
    model_path = './sign-language-1.h5'
    label_path = 'sign-language-model-1.pkl'
    model, labels_dict = load_model_and_labels(model_path, label_path)
    print(labels_dict)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to capture image")
            break

        frame = process_frame(frame, hands, draw_util, frame_data, model, labels_dict)

        cv2.imshow('Hand Sign Recognition', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
