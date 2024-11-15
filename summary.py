import akshare as ak
import cair_stock as cs
import constant.eastmoney_constant as const
import cointegration as co
import strategy.MeanReversionStrategyBaseResiduals as mr
import time

# 时间范围
START_DATE = "20190101"
END_DATE = "20241115"

base_stocks = ["000651", "600036", "600519", "601318"]

# 获取沪深300所有股票信息
stocks = cs.index_contain_stocks(symbol_code = "000300");
stock_code_2_info = {}
for index, row in stocks.iterrows():
    stock_code_2_info[row["成分券代码"]] = row

# 获取所有a股编码
stock_codes = list(stock_code_2_info.keys())
length = len(stock_codes)

for stock_code_a in base_stocks:
    for j in range(0, length):
        stock_code_b = stock_codes[j]

        # 获取基础信息
        stock_daily_history_a = cs.stock_daily_history(symbol_code=stock_code_a, start_date=START_DATE, end_date=END_DATE)
        stock_daily_history_b = cs.stock_daily_history(symbol_code=stock_code_b, start_date=START_DATE, end_date=END_DATE)
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

        print(mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY]))
        print(stock_code_a, stock_code_b)

        # 睡眠100毫秒，防止请求过于频繁
        time.sleep(0.1)