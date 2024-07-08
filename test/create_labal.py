#!/usr/bin/env python
# coding:utf8
import logging
import pickle
import os
# 定义标签列表
label_list = []
for filename in os.listdir('../../tensor_fit/npyfiles/'):
    if filename.endswith('.npy'):  # 确保只处理.npy文件
        # 提取不包含扩展名的文件名作为键
        word = filename[:-4]
        label_list.append(word)
# 创建标签映射字典
label_map = {i: label for i, label in enumerate(label_list)}
print(label_map)
# # 保存标签映射到文件
with open('sign-language-model-1.pkl', 'wb') as f:
    pickle.dump(label_map, f)
