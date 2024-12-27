import logging.config
import yaml
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
# 加载数据库配置
DATABASE_URL = os.getenv('DATABASE_URL')

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file.read())
    GLOBAL_CONFIG = config


logging.config.dictConfig(config["logging"])