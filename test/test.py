import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import utils.date_utils as du
import math
from datetime import datetime, timedelta

now = datetime.now()
# 去年
last_year = now - timedelta(days = 365)

# 十年前
annual_report_dates = du.get_annual_report_dates(last_year, 0)

# 获取财务数据基础信息
stock_code_2_date_2_base_info = su.stock_2_date_base_info(annual_report_dates)
print(stock_code_2_date_2_base_info["600519"])