from peewee import Model, MySQLDatabase
import utils.util as util
import yaml
import os

current_script_directory = os.path.dirname(os.path.abspath(__file__))
relative_path = current_script_directory + "../../../"
PROJECT_DIR = os.path.abspath(relative_path)
CONFIG_DIR = PROJECT_DIR + "/config/"

def load_config(config_file=CONFIG_DIR + 'db.yaml'):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config['stock_analysis']

mysql_db = MySQLDatabase(**load_config())

class BaseModel(Model):
    class Meta:
        database = mysql_db