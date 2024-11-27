import utils.stock_utils as cs
import constant.eastmoney_constant as const
import strategy.mean_reversion_strategy_base_residuals as mr

# 股票编码A
STOCK_CODE_A = "600036"
# 股票编码B
STOCK_CODE_B = "002142"

# 时间范围
START_DATE = "20080101"
END_DATE = "20241115"

# 股票A的每日历史信息
stock_daily_history_a = cs.stock_daily_history(STOCK_CODE_A, START_DATE, END_DATE)
stock_daily_history_b = cs.stock_daily_history(STOCK_CODE_B, START_DATE, END_DATE)

print(stock_daily_history_a)
print(stock_daily_history_b)

stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
stock_daily_history_a = stock_merge_list[0]
stock_daily_history_b = stock_merge_list[1]

mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY])