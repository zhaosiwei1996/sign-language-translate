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
draw_util = mp.solutions.drawing_utils
frame_data = collections.deque(maxlen=25)
# init mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# open camera
cap = cv2.VideoCapture(0)
# load model
model = tf.keras.models.load_model('../train/sign-language-model.h5_1000fit_9994_058')
# load labal
with open('../train/sign-language-model.pkl', 'rb') as f:
    labels_dict = pickle.load(f)

while True:
    # write frame
    ret, frame = cap.read()
    # frame transfer to rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # check hands
    hands_results = hands.process(frame_rgb)
    # analysis-hands-xyz
    if hands_results.multi_hand_landmarks:
        hand_landmarks = hands_results.multi_hand_landmarks[0]
        for hand_landmarks in hands_results.multi_hand_landmarks:
            landmark_list = []
            for landmark in hand_landmarks.landmark:
                landmark_list.append([landmark.x, landmark.y, landmark.z])
                # image draw landmarks
                draw_util.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                         draw_util.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                         draw_util.DrawingSpec(color=(0, 0, 255), thickness=2))

            landmarks_array = np.array(landmark_list).flatten()
            frame_data.append(landmarks_array)
            if len(frame_data) == 25:
                model_input = np.expand_dims(np.array(frame_data).T, axis=0)
                predictions = model.predict(model_input)
                predicted_class = np.argmax(predictions)
                predicted_prob_percentage = predictions[0][predicted_class] * 100
                # respones analysis
                predicted_label = labels_dict[predicted_class]
                # predicted_text = '''word:{},probability:{}'''.format(predicted_label, predicted_prob_percentage)
                predicted_text = '''{}'''.format(predicted_label)

                logging.info(
                    "Predicted_class:{},Predicted_label:{},probability:{}".format(predicted_class, predicted_label,
                                                                                 predicted_prob_percentage))
                # put image
                cv2.putText(frame, predicted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # open camera windows
    cv2.imshow('cv2', frame)
    # input q exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# break camera and windows
cap.release()
cv2.destroyAllWindows()
