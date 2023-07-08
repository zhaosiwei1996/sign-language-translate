import cv2
import mediapipe as mp

# 初始化 MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

# 加载视频
video_path = 'F:\\signdata\\America-dataset\\videos\\01157.mp4'
cap = cv2.VideoCapture(video_path)

# 初始化手部和脸部模型
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 调整图像为 RGB 格式
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 处理手部姿势
    results_hands = hands.process(image_rgb)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # 获取手部关键点坐标
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                # 在图像中绘制手部关键点
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    # 处理脸部表情
    results_face = face_mesh.process(image_rgb)
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            # 获取脸部关键点坐标
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                # 在图像中绘制脸部关键点
                cv2.circle(image, (x, y), 2, (255, 0, 0), -1)

    # 显示结果
    cv2.imshow('Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
