import tensorflow as tf

input_shape = (271257, 7, 63)
x = tf.random.normal(input_shape)
conv1D = tf.keras.layers.Conv1D(10, 10, padding='same')  # 1是输出通道数，3是卷积核大小，不使用边界填充
max_pool_1d = tf.keras.layers.MaxPooling1D(pool_size=2, strides=1, padding='same')
y = conv1D(x)
y = max_pool_1d(y)
print(y)
