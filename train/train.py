import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
import datetime
import tensorflow as tf

# 假设 features 和 labels 是你的数据
features = np.load('npyfile/sourcefile/book.npy')
sourcelabels = ['book','xxx','xxxx','xxxx']  # 标签数据
labels = np.repeat(sourcelabels, features.shape[0])

print('Features shape:', features.shape)

# 将类别标签转换为 one-hot 编码
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)
labels = to_categorical(labels)

# 划分训练集和测试集
features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.2, random_state=42)

# 构建模型
model = Sequential([
    Flatten(input_shape=(features.shape[1],)),
    Dense(128, activation='relu'),
    Dense(len(label_encoder.classes_), activation='softmax')
])
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
# 编译模型
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 训练模型
model.fit(features_train, labels_train, epochs=50, batch_size=32, callbacks=[tensorboard_callback])
model.save('./sign-language-model.h5')
# 验证模型
loss, accuracy = model.evaluate(features_test, labels_test)
print('Test Accuracy: %f' % (accuracy * 100))
