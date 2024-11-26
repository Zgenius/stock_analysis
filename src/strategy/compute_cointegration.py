import utils.stock_utils as cs
import constant.eastmoney_constant as const

# 获取a股所有股票信息
stock_code_2_info = cs.stock_code_2_info()
# 获取所有a股编码
stock_codes = list(stock_code_2_info.keys())
length = len(stock_codes)

for i in range(length - 1):
    for j in range(i + 1, length):
        stock_code_a = stock_codes[i]
        stock_code_b = stock_codes[j]
        print(stock_codes[i], stock_codes[j], stock_code_2_info[stock_code_a][const.STOCK_NAME], stock_code_2_info[stock_code_b][const.STOCK_NAME])

        # 股票A的每日历史信息
        stock_daily_history_a = ak.stock_zh_a_hist(symbol=stock_code_a, period="daily", start_date=START_DATE, end_date=END_DATE, adjust="qfq")
        # 股票B的每日历史信息
        stock_daily_history_b = ak.stock_zh_a_hist(symbol=stock_code_b, period="daily", start_date=START_DATE, end_date=END_DATE, adjust="qfq")