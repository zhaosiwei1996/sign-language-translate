import cv2

# 创建一个 VideoCapture 对象
video = cv2.VideoCapture(r'F:\\signdata\\\WLASL\\videos\\02105.mp4')

# 获取视频总帧数
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

print(total_frames)

# 最后记得释放 VideoCapture 对象
video.release()
