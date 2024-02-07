## 基于mediapipe进行手语翻译的研究

Study on sign language translation based on mediapipe
-----

## 技术栈

Technology stack
-----
开发语言Development language:Python3.10

模型训练Model training:tensorflow

画像识别Portrait recognition:mediapipe

服务端框架Server framework:sanic

通信协议Communication protocol:http post

## 目录结构

Directory structure
-----

| 目录名/文件名&目录名Directory name/file name & Directory name | 说明Instructions                                                |
|------------------------------------------------------|---------------------------------------------------------------|
| prod-web/static                                      | 静态资源Static resource css,js                                    |
| prod-web/templates                                   | h5                                                            |
| prob-web/main.py                                     | sanic server                                                  |
| prod-web/utils.py                                    | 工具类Utility class                                              |
| prod-web/config.py                                   | 配置文件config file                                               |
| test/localcamera.py                                  | 本地摄像头测试local camera test                                      |
| test/create_labal.py                                 | 创建标签create label                                              |
| test/utils.py                                        | 工具类Utility class                                              |
| train/huangxuan                                      | 黄玄的代码huangxuan code                                           |
| train/analysis-landmarks-hands.py                    | 从数据集中抽取手部坐标点Hand coordinates were extracted from the data set |
| train/config.py                                      | 配置文件config file                                               |
| train/checkanalysisresp.py                           | 检查分析结果是否有遗漏Check the analysis results for omissions           |
| train/old/                                           | 旧文件old file                                                   |
| prod/                                                | flask server deprecated（传输视频的方案,弃用）                           |
