#!/usr/bin/env python
# coding:utf8
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
import datetime

data = []
labels = []
label_data_dict = {
    'before': np.load('./npyfile/sourcefile/before.npy'),
    'book': np.load('./npyfile/sourcefile/book.npy'),
    'chair': np.load('./npyfile/sourcefile/chair.npy'),
    'computer': np.load('./npyfile/sourcefile/computer.npy'),
    'drink': np.load('./npyfile/sourcefile/drink.npy'),
    'go': np.load('./npyfile/sourcefile/go.npy')
}
for label, arr in label_data_dict.items():
    data.extend(arr)
    labels.extend([label] * len(arr))

# 转换为 numpy 数组 数据和标签
data = np.array(data)
labels = np.array(labels)

# 数据集划分为训练集、验证集和测试集
features_train, features_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2,
                                                                            random_state=42)

# 标签转换
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels_train)

model = Sequential([
    # 第一层卷积
    Conv1D(256, 100, activation='relu', padding='same', input_shape=(data.shape[1], 1)),  # 第一层1D卷积层
    MaxPooling1D(2, padding='same', strides=2),  # 第一层1D池化层
    Dropout(0.2),  # 第一层丢弃层
    # 第二层卷积
    Conv1D(128, 100, activation='relu', padding='same', input_shape=(data.shape[1], 1)),  # 第二层1D卷积层
    MaxPooling1D(1, padding='same', strides=1),  # 第二层1D池化层
    Dropout(0.2),  # 第二层丢弃层
    # 全连接层
    Flatten(),  # 将卷积层的输出扁平化，以便输入全连接层
    Dense(256, activation='relu'),  # 全连接层
    Dropout(0.2),  # 丢弃层
    Dense(128, activation='relu'),  # 全连接层
    Dropout(0.2),  # 丢弃层
    Dense(len(label_encoder.classes_), activation='relu'),  # 输出层
    Dropout(0.2)  # 丢弃层
])

# 打印卷积层信息
model.summary()
# 编译模型
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# 开启日志
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
# 训练模型
history = model.fit(features_train, encoded_labels, epochs=50, batch_size=2048, callbacks=[tensorboard_callback])

# 保存模型
model.save('./sign-language-model.h5')

# 验证模型
loss, accuracy = model.evaluate(features_test, encoded_labels)
print('Test Accuracy: %f' % (accuracy * 100))
# 保存标签编码器
with open('./sign-language-model.pkl', 'wb') as f:
    pickle.dump(encoded_labels, f)

# 绘制时间曲线图
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# 绘制损失函数曲线
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
