import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s [%(funcName)s]-%(process)d %(message)s')
logger = logging.getLogger(__name__)

# 指定英语单词
wordlistfile = "./1-100word.txt"

# 数据文件位置
viddir = r"F:\\signdata\\WLASL\\videos\\"

# 数据说明文件位置
worddir = r"F:\\signdata\\WLASL\\info.json"

# mysql配置
dbhost = "192.168.3.110"
dbuser = "zhaosiwei"
dbpassword = "111111"
dbname = "trainlandmark"

# 自动建表语句
createtablesql = """id int auto_increment NOT NULL COMMENT '自增id',
	videoid int NOT NULL COMMENT '视频id',
	face int NULL COMMENT '1代表为脸,0为不是',
	both_hands int NULL COMMENT '1代表为手,0为不是',
	x_landmark float NOT NULL COMMENT 'x坐标landmark',
	y_landmark float NOT NULL COMMENT 'y坐标landmark',
	z_landmark float NOT NULL COMMENT 'z坐标landmark',
	create_time datetime DEFAULT CURRENT_TIMESTAMP  NOT NULL COMMENT '创建时间',
	CONSTRAINT `PRIMARY` PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci
COMMENT='';
"""

# 并行分析数
processes = 12

# mediapipe配置
# 全局配置
static_image_mode = False
min_detection_confidence = 0.5

# 脸部识别
refine_landmarks = True
# 手部识别
max_num_hands = 2
min_tracking_confidence = 0.5
