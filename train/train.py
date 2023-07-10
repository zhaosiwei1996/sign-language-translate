#!/usr/bin/env python
# coding:utf8
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf
import datetime


def train():
    data = []
    labels = []
    label_data_dict = {
        'book': np.load('./book.npy'),
        'computer': np.load('./computer.npy'),
        'drink': np.load('./drink.npy'),
        'go': np.load('./go.npy')
    }
    for label, arr in label_data_dict.items():
        data.extend(arr)
        labels.extend([label] * len(arr))
    # 转换为 numpy 数组
    data = np.array(data)
    labels = np.array(labels)
    print(data.shape)
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    num_classes = len(set(labels))
    X_train, X_test, y_train, y_test = train_test_split(data, encoded_labels, test_size=0.2, random_state=42)
    # 建立模型
    model = tf.keras.Sequential([
        layers.Flatten(input_shape=(131, data.shape[0], 3)),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    # model = Sequential([
    #     Dense(128, activation='relu', input_shape=(None, data.shape[0], 3)),
    #     Dense(64, activation='relu'),
    #     Dense(num_classes, activation='softmax'),
    # ])

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    # 编译模型
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.summary()
    # 模型训练
    model.fit(X_train, y_train, epochs=50, batch_size=30, callbacks=[tensorboard_callback])
    # 模型保存
    model.save('./sign-language-model.h5')
    # 验证模型
    model.evaluate(X_test, y_test)


if __name__ == '__main__':
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
    train()
