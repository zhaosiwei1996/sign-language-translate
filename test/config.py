import logging

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] %(asctime)s [%(funcName)s]-%(process)d %(message)s')
logger = logging.getLogger(__name__)

# 指定英语单词list
# wordlistfile = "./1.txt"
wordlistfile = "./allwords.txt"

# 数据文件位置
viddir = r"F:\\signdata\\\WLASL\\videos\\"
# 目录分割
splitnum = 4

# 数据说明文件位置
worddir = r"F:\\signdata\\WLASL\\info.json"

# mysql配置
# dbhost = "192.168.3.110"
dbhost = "localhost"
dbuser = "root"
dbpassword = "111111"
dbname = "trainlandmark"

# 自动建表语句
createtablesql = """id int auto_increment NOT NULL COMMENT '自增id',
	videoid int NOT NULL COMMENT '视频id',
	hand_frame_count int NOT NULL COMMENT '手部动作帧号',
	video_total_frames int NOT NULL COMMENT '视频总帧数',

    wrist_x float NOT NULL COMMENT 'wrist_x_landmark',
    wrist_y float NOT NULL COMMENT 'wrist_y_landmark',
    wrist_z float NOT NULL COMMENT 'wrist_z_landmark',
	
    thumb_cmc_x float NOT NULL COMMENT 'thumb_cmc_x_landmark',
    thumb_cmc_y float NOT NULL COMMENT 'thumb_cmc_y_landmark',
    thumb_cmc_z float NOT NULL COMMENT 'thumb_cmc_z_landmark',
	
    thumb_mcp_x float NOT NULL COMMENT 'thumb_mcp_x_landmark',
    thumb_mcp_y float NOT NULL COMMENT 'thumb_mcp_y_landmark',
    thumb_mcp_z float NOT NULL COMMENT 'thumb_mcp_z_landmark',
	
    thumb_ip_x float NOT NULL COMMENT 'thumb_ip_x_landmark',
    thumb_ip_y float NOT NULL COMMENT 'thumb_ip_y_landmark',
    thumb_ip_z float NOT NULL COMMENT 'thumb_ip_z_landmark',
	
    thumb_tip_x float NOT NULL COMMENT 'thumb_tip_x_landmark',
    thumb_tip_y float NOT NULL COMMENT 'thumb_tip_y_landmark',
    thumb_tip_z float NOT NULL COMMENT 'thumb_tip_z_landmark',
	
    index_finger_mcp_x float NOT NULL COMMENT 'index_finger_mcp_x_landmark',
    index_finger_mcp_y float NOT NULL COMMENT 'index_finger_mcp_y_landmark',
    index_finger_mcp_z float NOT NULL COMMENT 'index_finger_mcp_z_landmark',
	
    index_finger_pip_x float NOT NULL COMMENT 'index_finger_pip_x_landmark',
    index_finger_pip_y float NOT NULL COMMENT 'index_finger_pip_y_landmark',
    index_finger_pip_z float NOT NULL COMMENT 'index_finger_pip_z_landmark',
	
    index_finger_dip_x float NOT NULL COMMENT 'index_finger_dip_x_landmark',
    index_finger_dip_y float NOT NULL COMMENT 'index_finger_dip_y_landmark',
    index_finger_dip_z float NOT NULL COMMENT 'index_finger_dip_z_landmark',
	
    index_finger_tip_x float NOT NULL COMMENT 'index_finger_tip_x_landmark',
    index_finger_tip_y float NOT NULL COMMENT 'index_finger_tip_y_landmark',
    index_finger_tip_z float NOT NULL COMMENT 'index_finger_tip_z_landmark',
	
    middle_finger_mcp_x float NOT NULL COMMENT 'middle_finger_mcp_x_landmark',
    middle_finger_mcp_y float NOT NULL COMMENT 'middle_finger_mcp_y_landmark',
    middle_finger_mcp_z float NOT NULL COMMENT 'middle_finger_mcp_z_landmark',
	
    middle_finger_pip_x float NOT NULL COMMENT 'middle_finger_pip_x_landmark',
    middle_finger_pip_y float NOT NULL COMMENT 'middle_finger_pip_y_landmark',
    middle_finger_pip_z float NOT NULL COMMENT 'middle_finger_pip_z_landmark',
	
    middle_finger_dip_x float NOT NULL COMMENT 'middle_finger_dip_x_landmark',
    middle_finger_dip_y float NOT NULL COMMENT 'middle_finger_dip_y_landmark',
    middle_finger_dip_z float NOT NULL COMMENT 'middle_finger_dip_z_landmark',
	
    middle_finger_tip_x float NOT NULL COMMENT 'middle_finger_tip_x_landmark',
    middle_finger_tip_y float NOT NULL COMMENT 'middle_finger_tip_y_landmark',
    middle_finger_tip_z float NOT NULL COMMENT 'middle_finger_tip_z_landmark',
	
    ring_finger_mcp_x float NOT NULL COMMENT 'ring_finger_mcp_x_landmark',
    ring_finger_mcp_y float NOT NULL COMMENT 'ring_finger_mcp_y_landmark',
    ring_finger_mcp_z float NOT NULL COMMENT 'ring_finger_mcp_z_landmark',
	
    ring_finger_pip_x float NOT NULL COMMENT 'ring_finger_pip_x_landmark',
    ring_finger_pip_y float NOT NULL COMMENT 'ring_finger_pip_y_landmark',
    ring_finger_pip_z float NOT NULL COMMENT 'ring_finger_pip_z_landmark',
	
    ring_finger_dip_x float NOT NULL COMMENT 'ring_finger_dip_x_landmark',
    ring_finger_dip_y float NOT NULL COMMENT 'ring_finger_dip_y_landmark',
    ring_finger_dip_z float NOT NULL COMMENT 'ring_finger_dip_z_landmark',
	
    ring_finger_tip_x float NOT NULL COMMENT 'ring_finger_tip_x_landmark',
    ring_finger_tip_y float NOT NULL COMMENT 'ring_finger_tip_y_landmark',
    ring_finger_tip_z float NOT NULL COMMENT 'ring_finger_tip_z_landmark',
	
    pinky_mcp_x float NOT NULL COMMENT 'pinky_mcp_x_landmark',
    pinky_mcp_y float NOT NULL COMMENT 'pinky_mcp_y_landmark',
    pinky_mcp_z float NOT NULL COMMENT 'pinky_mcp_z_landmark',
	
    pinky_pip_x float NOT NULL COMMENT 'pinky_pip_x_landmark',
    pinky_pip_y float NOT NULL COMMENT 'pinky_pip_y_landmark',
    pinky_pip_z float NOT NULL COMMENT 'pinky_pip_z_landmark',
	
    pinky_dip_x float NOT NULL COMMENT 'pinky_dip_x_landmark',
    pinky_dip_y float NOT NULL COMMENT 'pinky_dip_y_landmark',
    pinky_dip_z float NOT NULL COMMENT 'pinky_dip_z_landmark',
	
    pinky_tip_x float NOT NULL COMMENT 'pinky_tip_x_landmark',
    pinky_tip_y float NOT NULL COMMENT 'pinky_tip_y_landmark',
    pinky_tip_z float NOT NULL COMMENT 'pinky_tip_z_landmark',
	
	create_time datetime DEFAULT CURRENT_TIMESTAMP  NOT NULL COMMENT '创建时间',
	CONSTRAINT `PRIMARY` PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci
COMMENT='';
"""

# 手部坐标名称
hands_nameslist = ['wrist', 'thumb_cmc', 'thumb_mcp', 'thumb_ip', 'thumb_tip', 'index_finger_mcp', 'index_finger_pip',
                   'index_finger_dip', 'index_finger_tip', 'middle_finger_mcp', 'middle_finger_pip',
                   'middle_finger_dip', 'middle_finger_tip', 'ring_finger_mcp', 'ring_finger_pip', 'ring_finger_dip',
                   'ring_finger_tip', 'pinky_mcp', 'pinky_pip', 'pinky_dip', 'pinky_tip']

# 并行分析数
processes = 40

# mediapipe配置
# 全局配置
static_image_mode = False
min_detection_confidence = 0.5

# 脸部识别
refine_landmarks = True
# 手部识别
max_num_hands = 2
min_tracking_confidence = 0.5
