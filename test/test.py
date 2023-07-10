import cv2
import mediapipe as mp
import numpy as np

# 初始化 MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

# 加载视频
video_path = 'F:\\signdata\\\WLASL\\videos\\00836.mp4'
cap = cv2.VideoCapture(video_path)

# 初始化手部和脸部模型
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
landmarks = []

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 调整图像为 RGB 格式
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 处理脸部表情
    results_face = face_mesh.process(image_rgb)
    # 处理手部姿势
    results_hands = hands.process(image_rgb)

    if results_hands.multi_hand_landmarks is not None and results_face.multi_face_landmarks is not None:
        single_frame_landmarks = []
        for hand_landmarks in results_hands.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                single_frame_landmarks.extend([lm.x, lm.y, lm.z])
        for face_landmarks in results_face.multi_face_landmarks:
            for id, lm in enumerate(face_landmarks.landmark):
                single_frame_landmarks.extend([lm.x, lm.y, lm.z])
        landmarks.append(single_frame_landmarks)
    # 显示结果
    cv2.imshow('Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
landmarks = np.array(landmarks)
print(landmarks)
