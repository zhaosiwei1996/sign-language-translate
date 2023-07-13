import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout

# 假设序列长度为 seq_length
seq_length = 271257  # 应该根据你的实际数据来设置

# 构建模型
model = Sequential([
    Conv1D(32, 3, activation='relu', padding='same', input_shape=(seq_length, 63)),  # 第一层1D卷积层
    MaxPooling1D(2),  # 第一层1D池化层
    Dropout(0.5),  # 第一层丢弃层，丢弃率为0.5
    Conv1D(64, 3, activation='relu', padding='same'),  # 第二层1D卷积层
    MaxPooling1D(2),  # 第二层1D池化层
    Dropout(0.5),  # 第二层丢弃层，丢弃率为0.5
    Flatten(),  # 将卷积层的输出扁平化，以便输入全连接层
    Dense(128, activation='relu'),  # 全连接层
    Dropout(0.5),  # 在全连接层后添加一个丢弃层
    Dense(6, activation='softmax')  # 输出层，假设 num_classes 是你的类别数量
])

# 编译模型
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 查看模型结构
model.summary()
