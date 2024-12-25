import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import utils.date_utils as du
import math
from datetime import datetime, timedelta

START_DATE = "20241201"
END_DATE = datetime.now().strftime("%Y%m%d")
stock_code = "600519"

history = su.stock_daily_history(stock_code, START_DATE, END_DATE)
print(history)