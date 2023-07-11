#!/usr/bin/env python
# coding:utf8
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from utils import *
import numpy as np
import tensorflow as tf
import config
import logging


def train(labels, landmarks):
    # 将文本标签编码为数字
    encoder = LabelEncoder()
    labels = encoder.fit_transform(labels)
    # 切分训练集和测试集,0.2为80%训练,20%测试
    X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.2, random_state=42)
    # 建立模型
    model = Sequential([
        Flatten(input_shape=(landmarks.shape[1],)),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(len(encoder.classes_), activation='softmax')  # 类别数
    ])
    # 编译模型
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    # 模型训练
    model.fit(X_train, y_train, epochs=10)
    # 模型保存
    model.save('./sign-language-model.h5_20230710')
    # 验证模型
    model.evaluate(X_test, y_test)


if __name__ == '__main__':
    single_frame_landmarks = []
    landmarks = []
    wordlist = ['book', 'computer', 'drink', 'go']
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    for word in wordlist:
        starttime = BaseUtils.get_timestamp()
        logging.info("正在查询:{} 单词".format(word))
        queryselect = mysql_tool.select("t_{}".format(word), "x_landmark,y_landmark,z_landmark")
        for resp1 in queryselect:
            single_frame_landmarks.extend(resp1)
        endtime = BaseUtils.get_timestamp()
        logging.info("查询完成:{} 单词 耗时:{}".format(word, str(endtime - starttime)))
    landmarks.append(single_frame_landmarks)
    np.array(landmarks)
    print(single_frame_landmarks)
    mysql_tool.close()

    # 加载训练
    train(wordlist, landmarks)
