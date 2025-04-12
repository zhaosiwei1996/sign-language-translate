#!/usr/bin/env python
# coding:utf8
from utils import *
import numpy as np
import pandas as pd
import multiprocessing
import config
import logging


def get_reflection(src, tlen):  # return [src-reversed][src][src-r]...
    x = src.copy()
    x = np.flip(x, axis=0)
    ret = x.copy()
    while len(ret) < tlen:
        x = np.flip(x, axis=0)
        ret = np.concatenate((ret, x), axis=0)
    ret = ret[:tlen]
    return ret


def pad_to_window(slice, window):
    if len(slice) >= window:
        return slice
    left_len = (window - len(slice)) // 2 + (window - len(slice)) % 2
    right_len = (window - len(slice)) // 2
    left = np.flip(get_reflection(np.flip(slice, axis=0), left_len), axis=0)
    right = get_reflection(slice, right_len)
    slice = np.concatenate([left, slice, right], axis=0)
    assert len(slice) == window
    return slice


def divide_clip(input, window, window_step, divide):
    if not divide:  # return the whole clip
        t = ((input.shape[0]) // 4) * 4 + 4
        t = max(t, 12)
        if input.shape[0] < t:
            input = pad_to_window(input, t)
        return [input]
    windows = []
    for j in range(0, len(input) - window + 1, window_step):
        slice = input[j: j + window].copy()  # remember to COPY!!
        if len(slice) < window:
            slice = pad_to_window(slice, window)
        windows.append(slice.T)
    return windows


def worker(file):
    # 25码率
    win = 25
    # 步长 帧率 5
    step = 5
    coverdatapath = r"./npyfile/2024head-data-npy1"
    logging.info('开始分割手语单词数据:' + file)
    starttime = BaseUtils.get_timestamp()
    data = pd.read_excel(os.path.join(r"train/npyfile/2024head-data1/", file), header=None, engine="openpyxl").iloc[1:, 1:].values
    data = divide_clip(data, win, step, True)
    np.save(os.path.join(coverdatapath, file[:-5]), data)
    endtime = BaseUtils.get_timestamp()
    logging.info(f"{os.path.join(coverdatapath, file[:-5])}.npy保存完成,耗时: {endtime - starttime}")


if __name__ == '__main__':
    # 线程池
    threadlist = []
    pool = multiprocessing.Pool(processes=50)
    for root, dirs, files in os.walk(r"train/npyfile/2024head-data1/"):
        for file in files:
            if file.endswith('.xlsx'):
                threadlist.append(file)

    # for threadlist
    tasks = [i for i in threadlist]
    # start worker
    pool.map(worker, tasks)
    # close thread pool
    pool.close()
    pool.join()
