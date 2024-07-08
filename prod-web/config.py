import logging
import datetime

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s [%(funcName)s]-%(process)d %(message)s')
logger = logging.getLogger(__name__)

hostip = '0.0.0.0'
listport = 5000
modelfilepath = '../train/sign-language-model.h5_1000fit_9994_058'
labalfilepath = '../train/sign-language-model-1.pkl'
accesslogspath = "./services_accesslogs_{}.log".format(datetime.datetime.now().strftime("%Y%m%d"))
businesslogspath = "./services_businesslogs_{}.log".format(datetime.datetime.now().strftime("%Y%m%d"))
