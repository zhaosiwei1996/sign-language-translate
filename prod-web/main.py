from sanic import Sanic, response
from sanic_cors import CORS
from utils import *  # tools class
import numpy as np
import tensorflow as tf
import collections
import pickle
import config  # config file
import logging

app = Sanic("sign-language")
CORS(app)
# load model
frame_data = collections.deque(maxlen=25)
model = tf.keras.models.load_model(config.modelfilepath)
# load label
with open(config.labalfilepath, 'rb') as f:
    labels_dict = pickle.load(f)


# analysis-hands-model
def modelload():
    model_input = np.expand_dims(np.array(frame_data).T, axis=0)
    predictions = model.predict(model_input)
    predicted_class = np.argmax(predictions)
    predicted_prob_percentage = predictions[0][predicted_class] * 100
    # if predicted_prob_percentage < 100:
    #     continue
    #
    predicted_label = labels_dict[predicted_class]
    logging.info("Predicted_class:{},Predicted_label:{},Preprocess:{}".format(predicted_class, predicted_label,
                                                                              predicted_prob_percentage))
    return predicted_label, predicted_prob_percentage


# api interface
@app.post('/api/landmark')
async def landmarks_data(request):
    data = BaseUtils.string_to_json(request.body)
    landmark_list = []
    for landmarks in data['landmarks']:
        landmark_list.append([landmarks['x'], landmarks['y'], landmarks['z']])
    # print(landmark_list)
    frame_data.append(np.array(landmark_list).flatten())
    if len(frame_data) == 25:
        starttime = BaseUtils.get_timestamp()
        predicted_label, predicted_prob_percentage = modelload()
        endtime = BaseUtils.get_timestamp()
        BaseUtils.save_business_logs(request.ip, request.path, predicted_label, endtime - starttime,
                                     predicted_prob_percentage)

        return response.json(BaseUtils.send_default_info(200, request.ip, request.path, predicted_label))
    else:
        return response.json(BaseUtils.send_default_info(200, request.ip, request.path, "please wait..."))


# test api interface
@app.get("/")
async def hello_world(request):
    return response.json(BaseUtils.send_default_info(200, request.ip, request.path, "hello world"))


if __name__ == '__main__':
    app.run(port=config.listport, host=config.hostip, debug=False, access_log=True, workers=6)
