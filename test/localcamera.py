import cv2
import tensorflow as tf
import numpy as np
import mediapipe as mp
from sklearn.preprocessing import LabelEncoder
import pickle

# 加载模型
model = tf.keras.models.load_model('../train/sign-language-model.h5')

# 加载标签编码器
with open('../train/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# 初始化 Mediapipe 手势识别
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 使用 MediaPipe 检测手部关键点
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # 将 landmark 数据转为模型需要的形式
            data = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])
            data = np.expand_dims(data, axis=0)

            # 判断坐标是否符合预期，这里假设所有坐标都应在0和1之间
            if np.all((data >= 0) & (data <= 1)):
                # 使用模型进行预测
                predictions = model.predict(data)
                class_id = np.argmax(predictions[0])

                # 使用标签编码器将类别 id 转化为原始的标签
                class_label = label_encoder.inverse_transform([class_id])

                # 在视频帧上显示预测的类别
                cv2.putText(frame, f"Predicted class: {class_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Coordinates not as expected. Skipping prediction...", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 显示图像
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
