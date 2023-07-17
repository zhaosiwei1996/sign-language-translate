import os
import cv2
import mediapipe as mp
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

pose_points = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT',
               'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB',
               'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

input_folder = r"C:\Users\harry\OneDrive\桌面\展示" # 修改为你的输入文件夹路径
output_folder = r"C:\Users\harry\OneDrive\桌面\来吧" # 修改为你的输出文件夹路径

for i in range(1, 21):  # 遍历subject1到subject20
    subfolder = f"subject{i}"
    subfolder_path = os.path.join(input_folder, subfolder)
    if not os.path.exists(subfolder_path):
        continue
    for root, dirs, files in os.walk(subfolder_path):
        for filename in files:
            if filename == 'carrying.mp4':
                filepath = os.path.join(root, filename)

                cap = cv2.VideoCapture(filepath)

                alldata = []

                with mp_holistic.Holistic(
                        static_image_mode=False,
                        smooth_landmarks=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5,
                        model_complexity=2)as holistic:
                    
                    counter = 0 # 初始化计数器

                    while cap.isOpened():

                        counter += 1 # 每次循环计数器加1

                        success, image = cap.read()
                        if not success:
                            print("false")
                            break

                        image.flags.writeable = False
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        results = holistic.process(image)
                        pose_landmarks = results.pose_world_landmarks

                        
                        if pose_landmarks is not None:
                            data_points = {}
                            for i in range(len(pose_points)):
                                data_points.update(
                                    {pose_points[i]+'_x': results.pose_world_landmarks.landmark[i].x ,
                                     pose_points[i]+'_y': results.pose_world_landmarks.landmark[i].y ,
                                     pose_points[i]+'_z': results.pose_world_landmarks.landmark[i].z,
                                     pose_points[i]+'_score': results.pose_world_landmarks.landmark[i].visibility}
                                     )
                                
                            alldata.append(data_points)

                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                        #2D画图（飘忽）
                        # mp_drawing.draw_landmarks(
                        #     image,
                        #     results.pose_world_landmarks,
                        #     mp_holistic.POSE_CONNECTIONS)

                        #3D画图
                        # mp_drawing.plot_landmarks(
                        #     results.pose_world_landmarks,
                        #     mp_pose.POSE_CONNECTIONS) 

                        cv2.imshow('MediaPipe Holistic', image)
                        if cv2.waitKey(10) & 0xFF == 27:
                            break
                    
                    print(f"视频 {filename} 循环了 {counter} 次") # 打印循环次数

                    df = pd.DataFrame(alldata)
                    output_dir = os.path.join(output_folder, root.replace(input_folder, '').strip('\\'))
                    os.makedirs(output_dir, exist_ok=True)
                    output_filename = os.path.join(output_dir, 'carrying.xlsx')
                    df.to_excel(output_filename)

                cap.release()
                cv2.destroyAllWindows()
                print(f"{output_filename} 已保存！") 