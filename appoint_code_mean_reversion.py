import akshare as ak
import cair_stock as cs
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import cointegration as co
import strategy.MeanReversionStrategyBaseResiduals as mr
import time

# 最小上市交易日
MIN_EXCHANGE_DAY_NUM = 750
# 时间范围
START_DATE = "20190101"
END_DATE = "20241115"

base_stocks = {"000651":"格力电器", "600036":"招商银行", "600519":"贵州茅台", "601318":"中国平安"}

# 获取沪深300所有股票信息
stocks = cs.index_contain_stocks(fc.CODE_ZZ_A500);
stock_code_2_info = {}
for index, row in stocks.iterrows():
    stock_code_2_info[row["成分券代码"]] = row

# 获取所有a股编码
stock_codes = list(stock_code_2_info.keys())
stock_code_length = len(stock_codes)

for stock_code_a in base_stocks:
    for j in range(0, stock_code_length):
        stock_code_b = stock_codes[j]

        # 获取基础信息
        stock_daily_history_a = cs.stock_daily_history(symbol_code=stock_code_a, start_date=START_DATE, end_date=END_DATE)
        stock_daily_history_b = cs.stock_daily_history(symbol_code=stock_code_b, start_date=START_DATE, end_date=END_DATE)
        if len(stock_daily_history_a) <= MIN_EXCHANGE_DAY_NUM or len(stock_daily_history_b) <= MIN_EXCHANGE_DAY_NUM:
            continue

        stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
        stock_daily_history_a = stock_merge_list[0]
        stock_daily_history_b = stock_merge_list[1]

        # 元素数量
        length = len(stock_daily_history_a);
        # 没有数据，或者上市日期小于MIN_EXCHANGE_DAY_NUM个交易日的就不计算了
        if length == 0 or length < MIN_EXCHANGE_DAY_NUM:
            continue

        mean_reversion_code = mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY])
        if mean_reversion_code == -1:
            continue

        print(mean_reversion_code)
        print(stock_code_a, base_stocks[stock_code_a], stock_code_b, stock_code_2_info[stock_code_b]["成分券名称"])

        # 睡眠100毫秒，防止请求过于频繁
        time.sleep(0.1)