#!/usr/bin/env python
# coding:utf8
import logging
import pickle

# 定义标签列表
label_list = ['before', 'book', 'chair', 'computer', 'drink', 'go']

# 创建标签映射字典
label_map = {i: label for i, label in enumerate(label_list)}
print(label_map)
# # 保存标签映射到文件
with open('./sign-language-model.pkl', 'wb') as f:
    pickle.dump(label_map, f)
