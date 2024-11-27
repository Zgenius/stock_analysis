import utils.stock_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
from context.market_context import market_context
from datetime import datetime, timedelta

now = datetime.now()
earliest_availability = now - timedelta(days = 365 * 5)
earliest_availability_str = earliest_availability.strftime("%Y%m%d")

filter_sector_names = [
    "证券",
    "保险",
    "房地产开发",
    "房地产服务",
    "中药",
    "医疗服务",
    "医疗器械",
    "贸易行业",
    "纺织服装",
    "农牧饲渔",
    "物流行业",
    "航空机场",
    "商业百货"
]
stock_codes = []
# 所有股票信息
stocks = cu.index_contain_stocks(fc.CODE_ZZ_A500)
for index, row in stocks.iterrows():
    stock_info = cu.stock_individual_info(row[const.FUND_CONTAINS_STOCK_CODE])
    stock_availability = datetime.strptime(str(cu.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY)), "%Y%m%d")
    # 如果上市时间不小于可接受的最早上市时间，就过滤掉
    if stock_availability > earliest_availability:
        continue

    # 过滤掉行业：医疗，地产，金融，汽车
    sector_name = cu.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_SECTOR)
    if sector_name in filter_sector_names:
        continue

    # 记录下满足条件的编码
    stock_codes.append(cu.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_CODE))
print(stock_codes)
exit(0)

length = len(stock_codes)

for i in range(length - 1):
    for j in range(i + 1, length):
        stock_code_a = stock_codes[i]
        stock_code_b = stock_codes[j]