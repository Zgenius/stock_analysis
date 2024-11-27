import utils.stock_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
from context.market_context import marketContext
from datetime import datetime, timedelta

now = datetime.now()
earliest_availability = now - timedelta(days = 365 * 10)
earliest_availability_str = earliest_availability.strftime("%Y%m%d")

# 所有股票信息
stocks = cu.index_contain_stocks(fc.CODE_ZZ_A500)
for index, row in stocks.iterrows():
    stock_info = cu.stock_individual_info(row[const.FUND_CONTAINS_STOCK_CODE])
    stock_availability = datetime.strptime(str(cu.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY)), "%Y%m%d")
    # 如果上市时间不小于可接受的最早上市时间，就过滤掉
    if stock_availability > earliest_availability:
        continue
    print(stock_info)
    exit(0)

# 获取所有a股编码
stock_codes = list(marketContext.STOCK_CODE_2_INFO.keys())
length = len(stock_codes)

for i in range(length - 1):
    for j in range(i + 1, length):
        stock_code_a = stock_codes[i]
        stock_code_b = stock_codes[j]