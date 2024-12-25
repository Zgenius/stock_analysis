import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import utils.date_utils as du
import math
from datetime import datetime, timedelta

stock_code = "600519"

rights = su.stock_individual_ex_rights_detail(stock_code)
for ignore, right in rights.iterrows():
    print(right)
    # exit()