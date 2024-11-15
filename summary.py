import akshare as ak
import cair_stock as cs
import constant.eastmoney_constant as const
import cointegration as co
import time

# 时间范围
START_DATE = "20190101"
END_DATE = "20241115"

# 获取a股所有股票信息
stock_code_2_info = cs.stock_code_2_info()
# 获取所有a股编码
stock_codes = list(stock_code_2_info.keys())
length = len(stock_codes)

for i in range(length - 1):
    for j in range(i + 1, length):
        stock_code_a = stock_codes[i]
        stock_code_b = stock_codes[j]

        # 获取基础信息
        stock_daily_history_a = cs.stock_daily_history(symbol_code=stock_code_a, start_date=START_DATE, end_date=END_DATE, adjust="qfq")
        stock_daily_history_b = cs.stock_daily_history(symbol=stock_code_b, start_date=START_DATE, end_date=END_DATE, adjust="qfq")
        if len(stock_daily_history_a) <= 750 or len(stock_daily_history_b) <= 750:
            continue

        stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
        stock_daily_history_a = stock_merge_list[0]
        stock_daily_history_b = stock_merge_list[1]

        # 元素数量
        length = len(stock_daily_history_a);
        # 没有数据，或者上市日期小于750个交易日的就不计算了
        if length == 0 or length < 750:
            continue

        if co.cointegrate(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY]):
            print(stock_codes[i], stock_codes[j], stock_code_2_info[stock_code_a][const.STOCK_NAME], stock_code_2_info[stock_code_b][const.STOCK_NAME])

        # 睡眠100毫秒，防止请求过于频繁
        time.sleep(0.1)