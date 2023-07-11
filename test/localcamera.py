import cv2
import mediapipe as mp
import numpy as np
import tensorflow

# 加载训练好的模型
model = tensorflow.keras.models.load_model('../train/sign-language-model.h5_20230710')

# 初始化 MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 使用 MediaPipe 进行手部识别
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    # 分析结果
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 这里我们假设你的模型只需要手部的 XYZ 坐标
            hand = []
            for id, lm in enumerate(hand_landmarks.landmark):
                # 归一化的坐标转为像素坐标
                height, width, _ = frame.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                cz = lm.z

                # 收集坐标
                hand.extend([cx, cy, cz])

            # 转为模型需要的输入形状
            hand = np.array(hand).reshape((1, -1))

            # 使用模型预测
            prediction = model.predict(hand)
            label = np.argmax(prediction)

            # 在图像上显示预测
            cv2.putText(frame, str(label), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 显示图像
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
