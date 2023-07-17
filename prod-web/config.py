import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s [%(funcName)s]-%(process)d %(message)s')
logger = logging.getLogger(__name__)

hostip = '0.0.0.0'
listport = 5000
modelfilepath = '../train/sign-language-model.h5_1000fit_9994_058'
labalfilepath = '../train/sign-language-model.pkl'
