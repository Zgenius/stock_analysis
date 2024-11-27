import utils.stock_utils as su
import constant.eastmoney_constant as const
import strategy.mean_reversion_strategy_base_residuals as mr
from datetime import datetime

# 股票编码A
STOCK_CODE_A = "000651"
# 股票编码B
STOCK_CODE_B = "000333"

# 时间范围
START_DATE = "20080101"
END_DATE = datetime.now().strftime("%Y%m%d")

# 开始偏移量
START_OFFSET = 750
# 单次交易股票数
EXCHANGE_NUM = 1000

# 股票A的每日历史信息
stock_daily_history_a = su.stock_daily_history(STOCK_CODE_A, START_DATE, END_DATE)
stock_daily_history_b = su.stock_daily_history(STOCK_CODE_B, START_DATE, END_DATE)

stock_merge_list = su.sync_data_list(stock_daily_history_a, stock_daily_history_b)
stock_daily_history_a = stock_merge_list[0]
stock_daily_history_b = stock_merge_list[1]

stock_a_num = 10000
stock_b_num = 10000

ini_price_a = stock_daily_history_a.at[START_OFFSET, const.CLOSE_PRICE_KEY]
ini_price_b = stock_daily_history_b.at[START_OFFSET, const.CLOSE_PRICE_KEY]

end_price_a = 0
end_price_b = 0

# 余额
balance = 0

# 两次交易时间间隔
EXCHANGE_INTERVAL = 10
# 交易次数
exchange_times = 0

print("格力电器:", 10000, "美的集团:", 10000, ini_price_a, ini_price_b, 10000 * ini_price_a + 10000 * ini_price_b)
stock_length = stock_daily_history_a.shape[0]
for i in range(START_OFFSET, stock_length):
    res = mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY].iloc[0:i], stock_daily_history_b[const.CLOSE_PRICE_KEY].iloc[0:i])
    price_a = stock_daily_history_a.at[i, const.CLOSE_PRICE_KEY]
    price_b = stock_daily_history_b.at[i, const.CLOSE_PRICE_KEY]

    date_a = stock_daily_history_a.at[i, const.DATE]
    date_b = stock_daily_history_b.at[i, const.DATE]

    # 1 - 买入b，卖出a
    if res == 1:
        if stock_a_num >= EXCHANGE_NUM and exchange_times % EXCHANGE_INTERVAL == 0:
            # 算卖出钱数
            total = price_a * EXCHANGE_NUM
            # 卖出
            stock_a_num -= EXCHANGE_NUM
            # 买入余额
            stock_balance = total % price_b
            # 买入数量
            stock_b_num += (total - stock_balance) / price_b
            print(date_a, date_b)
            print("买入美的集团持仓: 格力电器：", stock_a_num, "美的集团:", stock_b_num,  price_a, price_b)

            # 余额汇总
            balance += stock_balance
            end_price_a = price_a
            end_price_b = price_b
        exchange_times += 1
        
    # 2 - 买入a, 卖出b
    elif res == 2:
        if stock_b_num > EXCHANGE_NUM and exchange_times % EXCHANGE_INTERVAL == 0:
            # 算卖出钱数
            total = price_b * EXCHANGE_NUM
            # 卖出
            stock_b_num -= EXCHANGE_NUM
            # 买入余额
            stock_balance = total % price_a
            # 买入数量
            stock_a_num += (total - stock_balance) / price_a
            print(date_a, date_b)
            print("买入格力电器持仓: 格力电器：", stock_a_num, "美的集团: ", stock_b_num, price_a, price_b)

            # 余额汇总
            balance += stock_balance
            end_price_a = price_a
            end_price_b = price_b
        exchange_times += 1
        

print("格力电器:", stock_a_num, "美的集团:", stock_b_num, end_price_a, end_price_b, stock_a_num * end_price_a + stock_b_num * end_price_b + balance)