import logging.config
import yaml
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
# 加载数据库配置
DATABASE_URL = os.getenv('DATABASE_URL')

# 加载日志配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file.read())
    GLOBAL_CONFIG = config

# 配置日志
logging.config.dictConfig(config["logging"])