import cv2
import mediapipe as mp

# 初始化MediaPipe手语识别模型
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取摄像头帧
    ret, frame = cap.read()

    # 将帧转换为RGB格式
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 检测手部
    results = mp_hands.process(frame_rgb)

    # 提取手部关键点
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                # 在图像上绘制关键点
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # 显示结果
    cv2.imshow('Hand Gesture Recognition', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和窗口
cap.release()
cv2.destroyAllWindows()
