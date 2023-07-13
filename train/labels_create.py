from sklearn.preprocessing import LabelEncoder
import pickle

# 假设这是你的标签数据
labels = ["book"]

# 创建一个标签编码器并用你的标签数据进行拟合
label_encoder = LabelEncoder()
label_encoder.fit(labels)

# 将标签编码器保存到文件
with open('./label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
