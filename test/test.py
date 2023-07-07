import cv2
import mediapipe as mp

# 初始化MediaPipe组件
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# 加载Holistic模型
mp_holistic_model = mp_holistic.Holistic(static_image_mode=False, min_detection_confidence=0.5,min_tracking_confidence=0.5)

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取视频帧
    ret, frame = cap.read()

    # 转换图像颜色空间为RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 调用MediaPipe进行手部追踪和动作识别
    results = mp_holistic_model.process(image)

    # 绘制手部关键点和骨骼连接
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    # 获取手部动作识别结果
    if results.right_hand_landmarks or results.left_hand_landmarks:
        # 根据需要处理手部动作识别结果
        # 这里仅打印出右手和左手的关键点坐标
        if results.right_hand_landmarks:
            print(results.right_hand_landmarks.landmark)
        if results.left_hand_landmarks:
            print(results.left_hand_landmarks.landmark)

    # 显示图像窗口
    cv2.imshow('MediaPipe Hand Action Detection', image)

    # 按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
