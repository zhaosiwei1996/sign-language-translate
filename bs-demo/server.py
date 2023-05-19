from flask import Flask, render_template
from flask_socketio import SocketIO
from logging.config import dictConfig
from utils import *
import mediapipe as mp
import cv2
import numpy as np
import base64

dictConfig({
    "version": 1,
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "level": "DEBUG",
            "formatter": "main_formatter"
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "main_formatter"
        }
    },
    "formatters": {
        "main_formatter": {
            "format": "[%(levelname)s] %(asctime)s [%(funcName)s] %(name)s %(message)s"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file_handler", "console_handler"]
    }
}
)

app = Flask(__name__)
socketio = SocketIO(app, compile=True)  # 开启socketio压缩

# 初始化MediaPipe
# mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)


@socketio.on('video_stream')
def handle_video_stream(image_data):
    # 将Base64编码的图像数据解码为图像
    starttime = BaseUtils.get_timestamp()
    encoded_data = image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 检测手部
    results = mp_hands.process(frame)
    # 提取手部关键点
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                # 在图像上绘制关键点
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # 测试点 是否将手部绘制捕获点
    # cv2.imwrite('./optput.jpg', frame)

    # 将绘制了手部动作的图像转换为Base64编码
    ret, buffer = cv2.imencode('.webp', frame)
    encoded_image = base64.b64encode(buffer)
    endtime = BaseUtils.get_timestamp()
    app.logger.info("ip:%s,流程处理耗时:%s" % (BaseUtils.get_client_ip(), str(endtime - starttime)))
    # 将结果返回给客户端
    socketio.emit('hand_gesture', encoded_image.decode('utf-8'))


@app.route('/')
def htmltest():
    return BaseUtils.send_default_info("hello world")


@app.route('/camera')
def index():
    app.logger.info(BaseUtils.get_client_ip())
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
