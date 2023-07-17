from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from logging.config import dictConfig
from utils import *
import mediapipe as mp
import numpy as np
import tensorflow as tf
import cv2
import base64
import config
import logging
import collections
import pickle

# 初始化flask,tensorflow日志配置
dictConfig(config.logsconfig)
logger = tf.get_logger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

# 初始化mediapipe、加载模型
# init mediapipe
mp_hands = mp.solutions.hands
draw_util = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# 加载模型、帧数加载到25
frame_data = collections.deque(maxlen=25)
model = tf.keras.models.load_model(config.modelfilepath)
# 加载pickle文件中的标签
with open(config.labalfilepath, 'rb') as f:
    labels_dict = pickle.load(f)
# 设置跨域,开启socketio压缩
# set cors domain,open socketio gzip
socketio = SocketIO(app, compile=True)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio.init_app(app, async_mode=None, cors_allowed_origins='*')


# model load
def modelload():
    model_input = np.array(frame_data).T
    model_input = np.expand_dims(model_input, axis=0)
    # 加载模型并预测
    predictions = model.predict(model_input)
    predicted_class = np.argmax(predictions)
    # 计算百分比
    predicted_prob_percentage = predictions[0][predicted_class] * 100
    # if predicted_prob_percentage < 100:
    #     continue
    # 输出匹配结果
    predicted_label = labels_dict[predicted_class]
    predicted_text = '''word:{}'''.format(predicted_label)
    app.logger.info(
        "Predicted_class:{},Predicted_label:{},Preprocess:{}".format(predicted_class, predicted_label,
                                                                     predicted_prob_percentage))
    return predicted_text


@app.route('/api/landmark', methods=['POST'])
def landmarks_data():
    data = request.get_json()
    landmark_list = []
    for landmarks in data['landmarks']:
        landmark_list.append([landmarks['x'], landmarks['y'], landmarks['z']])
    frame_data.append(np.array(landmark_list).flatten())
    if len(frame_data) == 25:
        predicted_text = modelload()
        app.logger.info(predicted_text)
        return BaseUtils.send_default_info(predicted_text), 200


@socketio.on('video_stream')
def handle_video_stream(image_data):
    encoded_data = image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    hands_results = hands.process(frame)
    starttime = BaseUtils.get_timestamp()
    if hands_results.multi_hand_landmarks:
        hand_landmarks = hands_results.multi_hand_landmarks[0]
        landmark_list = []
        for landmark in hand_landmarks.landmark:
            landmark_list.append([landmark.x, landmark.y, landmark.z])
            draw_util.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                     draw_util.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                     draw_util.DrawingSpec(color=(0, 0, 255), thickness=2))
        frame_data.append(np.array(landmark_list).flatten())
        if len(frame_data) == 25:
            predicted_text = modelload()
            # 显示在屏幕上
            cv2.putText(frame, predicted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    endtime = BaseUtils.get_timestamp()
    app.logger.info("client ip:%s,Processing time:%s" % (BaseUtils.get_client_ip(), str(endtime - starttime)))

    # 测试点 是否将手部绘制捕获点
    # cv2.imwrite('./optput.jpg', frame)
    ret, buffer = cv2.imencode('.webp', frame)
    encoded_image = base64.b64encode(buffer)
    socketio.emit('hand_gesture', encoded_image.decode('utf-8'))


@app.route('/')
def htmltest():
    # test page
    return BaseUtils.send_default_info("hello world")


@app.route('/camera')
def index():
    app.logger.info(BaseUtils.get_client_ip())
    return render_template('test.html')


if __name__ == '__main__':
    socketio.run(app, host=config.hostip, port=config.listport, debug=True)
