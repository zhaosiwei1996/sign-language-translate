import cv2

# 打开视频文件
video_path = 'F:\\signdata\\\WLASL\\videos\\00333.mp4'  # 视频文件的路径
cap = cv2.VideoCapture(video_path)

# 获取视频的帧数
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("视频帧数:", frame_count)

# 释放资源
cap.release()