#!/usr/bin/env python
# coding:utf8
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
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
# 转换为 numpy 数组
data = np.array(data)
labels = np.array(labels)
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
print(data.shape)
# 数据集划分为训练集、验证集和测试集
X_train, X_val, y_train, y_val = train_test_split(data, encoded_labels, test_size=0.2, random_state=42)

# 构建卷积神经网络模型
model = tf.keras.Sequential([
    # 第一层输入层
    tf.keras.layers.Conv1D(filters=8,  # 卷积层的输出通道数量,根据计算机性能填写
                           kernel_size=100,  # 卷积核的长度,单数
                           batch_input_shape=(63, data.shape[0], 25),
                           # 在tensorflow中,1维卷积操作为从上到下卷积,
                           # 第一个参数为有x个样本,第二个参数为有多少x列数据
                           # 在torch中为从左往右卷积
                           padding='same',  # 自动填充,在torch中需要自己计算
                           activation='relu'),  # 激活函数
    # 第一层池化
    tf.keras.layers.MaxPooling1D(pool_size=2, strides=1, padding='same'),
    # 第一层丢弃
    tf.keras.layers.Dropout(0.2),
    # 第二层 输出要减半
    tf.keras.layers.Conv1D(filters=4,  # 卷积层的输出通道数量,根据计算机性能填写
                           kernel_size=100,  # 卷积核的长度
                           batch_input_shape=(63, data.shape[0], 25),
                           # 在tensorflow中,1维卷积操作为从上到下卷积,
                           # 第一个参数为有x个样本,第二个参数为有多少x列数据
                           # 在torch中为从左往右卷积
                           padding='same',  # 自动填充
                           activation='relu',  # 激活函数

                           ),
    # 第二层池化
    tf.keras.layers.MaxPooling1D(pool_size=2, padding='same'),
    # 第二层丢弃
    tf.keras.layers.Dropout(0.2),
    # 全连接层,从卷积层到全连接层的过渡,二维转一维
    tf.keras.layers.Flatten(),
    # 输出特征的维度,输入自动判断
    tf.keras.layers.Dense(units=256, activation='relu'),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(data.shape[1], activation='relu'),
    tf.keras.layers.Dropout(0.2),

])
# 打印卷积层信息
model.summary()
# 编译模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# 开启日志
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# 训练模型
history = model.fit(X_train, y_train, epochs=50, batch_size=64, callbacks=[tensorboard_callback])

# 保存模型
model.save('./sign-language-model.h5')

# 保存标签编码器
with open('sign-language-model.pkl', 'wb') as f:
    pickle.dump(encoded_labels, f)
#
# # 绘制时间曲线图
# plt.plot(history.history['accuracy'], label='Train Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()
#
# # 绘制损失函数曲线
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
