#!/usr/bin/env python
# coding:utf8
from utils import *
import numpy as np
import config
import pandas as pd

if __name__ == '__main__':
    # 转换numarray数组list
    landmarks = []
    # 100个单词list
    wordlist = ['before']
    # wordlist = ['book', 'computer', 'drink', 'go']
    # 数据库连接
    mysql_tool = MySQLTool(config.dbhost, config.dbuser, config.dbpassword, config.dbname)
    mysql_tool.connect()
    # 遍历数据库,xyz数据提取出来
    for word in wordlist:
        query = mysql_tool.select("t_{}".format(word),
                                  "wrist_x, wrist_y, wrist_z, thumb_cmc_x, thumb_cmc_y, thumb_cmc_z, thumb_mcp_x, thumb_mcp_y, thumb_mcp_z, thumb_ip_x, thumb_ip_y, thumb_ip_z, thumb_tip_x, thumb_tip_y, thumb_tip_z, index_finger_mcp_x, index_finger_mcp_y, index_finger_mcp_z, index_finger_pip_x, index_finger_pip_y, index_finger_pip_z, index_finger_dip_x, index_finger_dip_y, index_finger_dip_z, index_finger_tip_x, index_finger_tip_y, index_finger_tip_z, middle_finger_mcp_x, middle_finger_mcp_y, middle_finger_mcp_z, middle_finger_pip_x, middle_finger_pip_y, middle_finger_pip_z, middle_finger_dip_x, middle_finger_dip_y, middle_finger_dip_z, middle_finger_tip_x, middle_finger_tip_y, middle_finger_tip_z, ring_finger_mcp_x, ring_finger_mcp_y, ring_finger_mcp_z, ring_finger_pip_x, ring_finger_pip_y, ring_finger_pip_z, ring_finger_dip_x, ring_finger_dip_y, ring_finger_dip_z, ring_finger_tip_x, ring_finger_tip_y, ring_finger_tip_z, pinky_mcp_x, pinky_mcp_y, pinky_mcp_z, pinky_pip_x, pinky_pip_y, pinky_pip_z, pinky_dip_x, pinky_dip_y, pinky_dip_z, pinky_tip_x, pinky_tip_y, pinky_tip_z")

        for resp in query:
            # print(resp)
            landmarks.append(resp)

    print(landmarks)

    df = pd.DataFrame(landmarks)
    df.to_excel('./npyfile/coverfile/before.xlsx')

    # np.save('npyfile/sourcefile/go.npy', np.array(landmarks))
