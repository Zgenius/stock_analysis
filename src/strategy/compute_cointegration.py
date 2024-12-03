import utils.stock_utils as su
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import strategy.stock_back_testing as st
from datetime import datetime, timedelta

"""
这个策略只适合同一行业或者行业板块指数基金和个股做均值回归
"""

now = datetime.now()
earliest_availability = now - timedelta(days = 365 * 5)
earliest_availability_str = earliest_availability.strftime("%Y%m%d")

annual_report_dates = [
    "20101231",
    "20111231",
    "20121231",
    "20131231",
    "20141231",
    "20151231",
    "20161231",
    "20171231",
    "20181231",
    "20191231",
    "20201231",
    "20211231",
    "20221231",
    "20231231",
]

# 需要过滤掉的行业
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
stocks = su.index_contain_stocks(fc.CODE_ZZ_A500)
for index, row in stocks.iterrows():
    stock_info = su.stock_individual_info(row[const.FUND_CONTAINS_STOCK_CODE])
    stock_availability = datetime.strptime(str(su.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY)), "%Y%m%d")
    # 如果上市时间不小于可接受的最早上市时间，就过滤掉
    if stock_availability > earliest_availability:
        continue

    # 过滤掉行业：医疗，地产，金融，汽车
    sector_name = su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_SECTOR)
    if sector_name in filter_sector_names:
        continue

    # 记录下满足条件的编码
    stock_codes.append(su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_CODE))
print(stock_codes)

satisfied_ROE_stock_codes = []
# 获取股票每年的ROE
stock_code_2_date_ROE = sim.stock_ROE(stock_codes, annual_report_dates)
print(stock_code_2_date_ROE)
for index, stock_code in enumerate(stock_codes):
    if stock_code not in stock_code_2_date_ROE:
        continue
    # 获取股票时间范围内的所有ROE
    date_2_ROE = stock_code_2_date_ROE[stock_code]

    # 跳过ROE过低股票的标记
    jump_stock_code = False
    for ROE in date_2_ROE.values():
        # ROE存在小于15就跳过这只股票
        if ROE < 15.0:
            jump_stock_code = True
            break

    # 满足ROE条件的记录下
    if not jump_stock_code:
        satisfied_ROE_stock_codes.append(stock_code)
print(satisfied_ROE_stock_codes)

length = len(satisfied_ROE_stock_codes)

for i in range(length - 1):
    for j in range(i + 1, length):
        stock_code_a = satisfied_ROE_stock_codes[i]
        stock_code_b = satisfied_ROE_stock_codes[j]

        stock_back = st.stock_back_testing()
        stock_back.run([stock_code_a, stock_code_b])
        split = ""
        for split_index in range(0, 100):
            split += "="
        print(split)