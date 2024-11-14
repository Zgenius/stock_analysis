import akshare as ak
import cair_calculate as cc
import cointegration as co
import cair_stock as cs
import eastmoney_constant as const

# 股票编码A
STOCK_CODE_A = "002142"
# 股票编码B
STOCK_CODE_B = "600036"

# 时间范围
START_DATE = "20210101"
END_DATE = "20241112"

# 资金
total = 100000
# 价差
gap = 2

# 股票A的每日历史信息
stock_daily_history_a = ak.stock_zh_a_hist(symbol=STOCK_CODE_A, period="daily", start_date=START_DATE, end_date=END_DATE, adjust="qfq")
# 股票B的每日历史信息
stock_daily_history_b = ak.stock_zh_a_hist(symbol=STOCK_CODE_B, period="daily", start_date=START_DATE, end_date=END_DATE, adjust="qfq")
# etf
# stock_daily_history_b = ak.fund_etf_hist_em(symbol=STOCK_CODE_B, period="daily", start_date=START_DATE, end_date=END_DATE, adjust="")


print(stock_daily_history_a)
print(stock_daily_history_b)

stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
stock_daily_history_a = stock_merge_list[0]
stock_daily_history_b = stock_merge_list[1]

# 元素数量
length = len(stock_daily_history_a);
if length == 0:
    exit(0)

# 统计周期开始价格
start_price_a = stock_daily_history_a[const.CLOSE_PRICE_KEY][0]
start_price_b = stock_daily_history_b[const.CLOSE_PRICE_KEY][0]
print(cc.calculate_std_dev(stock_daily_history_a[const.CLOSE_PRICE_KEY]))
print(co.cointegrate(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY]))

# 统计周期结束价格
end_price_a = stock_daily_history_a[const.CLOSE_PRICE_KEY][length - 1]
end_price_b = stock_daily_history_b[const.CLOSE_PRICE_KEY][length - 1]

# 循环计算
for i in range(0, length):
    # 股票A的涨跌幅
    price_fluctuation_a = stock_daily_history_a[const.FLUCTUATION_RANGE][i]
    # 股票B的涨跌幅
    price_fluctuation_b = stock_daily_history_b[const.FLUCTUATION_RANGE][i]
    # 股票当日涨跌幅差额
    difference = price_fluctuation_a - price_fluctuation_b

    num_geli = total / stock_daily_history_a[const.CLOSE_PRICE_KEY][i]
    num_zhaoshang = total / stock_daily_history_b[const.CLOSE_PRICE_KEY][i]