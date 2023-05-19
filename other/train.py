#!/usr/bin/env python
# coding:utf8
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s [%(funcName)s] %(message)s')
logger = logging.getLogger(__name__)


def enddata():
    return int(time.time())


def startdata():
    return int(time.time())


def worker():
    startmodel = startdata()
    logging.info('start model')
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))  # 根据手语分类数设置 num_classes
    endmodel = enddata()
    logging.info('model use time:' + str(endmodel - startmodel))
    # build
    startcompile = startdata()
    logging.info('start compile')
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    endcompile = enddata()
    logging.info('compile use time:' + str(endcompile - startcompile))
    startfit = startdata()
    logging.info('start fit')
    model.fit(train_generator,
              steps_per_epoch=train_generator.samples // batch_size,
              validation_data=validation_generator,
              validation_steps=validation_generator.samples // batch_size,
              epochs=epochs)
    endfit = enddata()
    logging.info('fit use data:' + str(endfit - startfit))
    model.save('./sign_language_model.h5')


if __name__ == '__main__':
    # 数据集
    train_data_dir = 'F:\\phoenix-2014.v3\\ASL_Dataset\\Train'
    # 测试
    validation_data_dir = 'F:\\phoenix-2014.v3\\ASL_Dataset\\Test'
    # 同时训练的样本数量
    batch_size = 50
    # 整个训练数据集完整地通过神经网络进行前向传播和反向传播的次数
    epochs = 50
    # 图像高
    image_height = 400
    # 图像宽
    image_width = 400
    # 分类任务中输出类别的数量
    num_classes = 28

    # 数据增强
    logging.info('start train_datagen')
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)
    validation_datagen = ImageDataGenerator(rescale=1. / 255)
    logging.info('start train_generator')
    train_generator = train_datagen.flow_from_directory(train_data_dir,
                                                        target_size=(image_height, image_width),
                                                        batch_size=batch_size,
                                                        class_mode='categorical')
    logging.info('start validation_generator')
    validation_generator = validation_datagen.flow_from_directory(validation_data_dir,
                                                                  target_size=(image_height, image_width),
                                                                  batch_size=batch_size,
                                                                  class_mode='categorical')
    worker()
