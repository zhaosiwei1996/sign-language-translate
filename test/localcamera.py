import mediapipe as mp
import tensorflow as tf
import cv2
import numpy as np

# 加载训练好的模型
model = tf.keras.models.load_model('../train/sign-language-model.h5')

# 初始化 MediaPipe Hand 处理器
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2)

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取摄像头帧
    ret, frame = cap.read()

    # 转换为 RGB 格式
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 将图像传递给 MediaPipe Hand 处理器进行手部关键点检测
    results = mp_hands.process(image)

    # 检测到手部时，获取关键点坐标
    if results.multi_hand_landmarks:
        # 提取关键点坐标
        landmarks = results.multi_hand_landmarks[0].landmark
        hand_keypoints = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks])

        # 调整关键点数据的形状
        hand_keypoints = np.reshape(hand_keypoints, (1, -1))  # 调整为 (1, 3 * num_keypoints)

        # 进行手势识别
        predictions = model.predict(hand_keypoints)
        predicted_class = np.argmax(predictions)

        # 在图像上绘制结果
        cv2.putText(frame, str(predicted_class), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 显示图像
    cv2.imshow('Hand Gesture Recognition', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
