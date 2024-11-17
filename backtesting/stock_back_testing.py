import akshare as ak
import cair_calculate as cc
import cair_stock as cs
import cair_fund as cf
import constant.eastmoney_constant as const
import strategy.MeanReversionStrategyBaseResiduals as mr

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

stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
stock_daily_history_a = stock_merge_list[0]
stock_daily_history_b = stock_merge_list[1]

stock_a_num = 10000
stock_b_num = 10000

ini_price_a = stock_daily_history_a.at[750, const.CLOSE_PRICE_KEY]
ini_price_b = stock_daily_history_b.at[750, const.CLOSE_PRICE_KEY]

end_price_a = 0
end_price_b = 0

# 余额
balance = 0

print("招商银行:", 10000, "宁波银行:", 10000, ini_price_a, ini_price_b, 10000 * ini_price_a + 10000 * ini_price_b)
stock_length = stock_daily_history_a.shape[0]
for i in range(750, stock_length):
    res = mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY].iloc[0:i], stock_daily_history_b[const.CLOSE_PRICE_KEY].iloc[0:i])
    price_a = stock_daily_history_a.at[i, const.CLOSE_PRICE_KEY]
    price_b = stock_daily_history_b.at[i, const.CLOSE_PRICE_KEY]

    date_a = stock_daily_history_a.at[i, const.DATE]
    date_b = stock_daily_history_b.at[i, const.DATE]

    # 1 - 买入b，卖出a
    if res == 1:
        if stock_a_num > 0:
            # 算卖出钱数
            total = price_a * stock_a_num
            # 卖出
            stock_a_num = 0
            # 买入余额
            stock_balance = total % price_b
            # 买入数量
            stock_b_num += (total - stock_balance) / price_b
            print(date_a, date_b)
            print("买入宁波银行持仓: 招商银行：", stock_a_num, "宁波银行:", stock_b_num,  price_a, price_b)

            # 余额汇总
            balance += stock_balance
            end_price_a = price_a
            end_price_b = price_b
    # 2 - 买入a, 卖出b
    elif res == 2:
        if stock_b_num > 0:
            # 算卖出钱数
            total = price_b * stock_b_num
            # 卖出
            stock_b_num = 0
            # 买入余额
            stock_balance = total % price_a
            # 买入数量
            stock_a_num += (total - stock_balance) / price_a
            print(date_a, date_b)
            print("买入招商银行持仓: 招商银行：", stock_a_num, "宁波银行: ", stock_b_num, price_a, price_b)

            # 余额汇总
            balance += stock_balance
            end_price_a = price_a
            end_price_b = price_b

print("招商银行:", stock_a_num, "宁波银行:", stock_b_num, end_price_a, end_price_b, stock_a_num * end_price_a + stock_b_num * end_price_b + balance)