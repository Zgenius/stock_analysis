import akshare as ak
import cair_calculate as cc
import cointegration as co
import cair_stock as cs
import cair_fund as cf
import constant.eastmoney_constant as const
import strategy.MeanReversionStrategyBaseResiduals as mr

# 股票编码A
STOCK_CODE_A = "600036"
# 股票编码B
STOCK_CODE_B = "512800"

# 时间范围
START_DATE = "20190101"
END_DATE = "20241112"

# 股票A的每日历史信息
stock_daily_history_a = cs.stock_daily_history(STOCK_CODE_A, START_DATE, END_DATE)
stock_daily_history_b = cf.fund_daily_history(STOCK_CODE_B, START_DATE, END_DATE)

print(stock_daily_history_a)
print(stock_daily_history_b)

stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
stock_daily_history_a = stock_merge_list[0]
stock_daily_history_b = stock_merge_list[1]

mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY])