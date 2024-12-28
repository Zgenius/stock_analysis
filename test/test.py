from model.stock_basic_info import StockBasicInfo
from time import sleep
import utils.stock_utils as su
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc

# 获取所有股票信息
stocks = su.index_contain_stocks(fc.CODE_ZZ_ALL)
print(stocks)