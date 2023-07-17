## 基于mediapipe进行手语翻译的研究

-----

## 技术栈

-----
开发语言:Python3.10

模型训练:tensorflow

画像识别:mediapipe

服务端框架:sanic

通信协议:http post

## 目录结构

-----

| 目录名/文件名&目录名                       | 说明                       |
|-----------------------------------|--------------------------|
| prod-web/static                   | 静态资源css,js               |
| prod-web/templates                | h5                       |
| prob-web/main.py                  | sanic server             |
| prod-web/utils.py                 | 工具类                      |
| prod-web/config.py                | 配置文件                     |
| test/localcamera.py               | 本地摄像头测试                  |
| test/create_labal.py              | 创建标签                     |
| test/utils.py                     | 工具类                      |
| train/huangxuan                   | 黄玄的代码                    |
| train/analysis-landmarks-hands.py | 从数据集中抽取手部坐标点             |
| train/config.py                   | 配置文件                     |
| train/checkanalysisresp.py        | 检查分析结果是否有遗漏              |
| train/old/                        | 旧文件                      |
| prod/                             | flask server（传输视频的方案,弃用） |
