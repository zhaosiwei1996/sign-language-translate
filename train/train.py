#!/usr/bin/env python
# coding:utf8
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
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
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    X_train, X_test, y_train, y_test = train_test_split(data, encoded_labels, test_size=0.2, random_state=42)

    model = tf.keras.Sequential([
        layers.Flatten(input_shape=(data.shape[0],)),
        layers.Dense(63, activation='relu'),
        layers.Dense(len(set(labels)), activation='softmax')
    ])
    # model = Sequential()
    # model.add(Dense(32, input_dim=63, activation='relu'))  # 输入层
    # model.add(Dense(64, activation='relu'))  # 隐藏层
    # model.add(Dense(data.shape[1], activation='softmax'))

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    # 编译模型
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    model.summary()
    # 模型训练
    model.fit(X_train, y_train, epochs=50, batch_size=64, callbacks=[tensorboard_callback])
    # 模型保存
    model.save('./sign-language-model.h5')
    # 验证模型
    # 评估模型
    _, accuracy = model.evaluate(X_test, y_test)
    print('Accuracy: %.2f' % (accuracy * 100))


if __name__ == '__main__':
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
    train()
