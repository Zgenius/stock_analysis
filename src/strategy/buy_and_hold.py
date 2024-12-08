import manager.stock_choice as sc
import utils.date_utils as du
import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import utils.util as util
import time
from model.grid_table import grid_table
from model.account import account
from datetime import datetime

"""
buy and hold 低估分批买入，高估分批卖出
"""

# 时间范围
START_DATE = "20140101"
END_DATE = datetime.now().strftime("%Y%m%d")
# END_DATE = "20211231"

BUY_POSITION = {
    0: 100,
    10: 90,
    20: 80,
    30: 50
}

SELL_POSITION = {
    99: 0,
    # 90: 50,
    # 80: 20,
    # 70: 10
}

# 选股
stock_codes = sc.stock_choice(10)
print(stock_codes)

# stock_codes = [
#     "000333", # 22%
#     "000651", # 26%
#     # "000661", # 18%
#     "002304", # 20%
#     "002415", # 19%
#     "300628", # 25%
#     # "600036", # 16%
#     "600519", # 30%
#     "600563", # 20%
#     # "600690", # 17%
#     # "600885", # 17%
#     "600887", # 20%
#     "603288", # 20%
#     "603605", # 25%
#     # "603833", # 15%
#     # "603899" # 15%
# ]

# 股票数量
stock_num = len(stock_codes)

# 初始化账户
user_account = account(1000000)
print(user_account)

# 初始化网格记录表
table = grid_table()

# 记录股票，买入的分位，每个分位买一次
stock_code_2_buy_rate = {}
# 记录股票，卖出的分位，每个分位卖一次
stock_code_2_sell_rate = {}

# 记录股票编码到指标类信息的映射
stock_code_2_indicator = {}
# 股票编码到历史数据的映射表
stock_code_2_history_info = {}
# 股票除权除息信息
stock_code_2_ex_rights = {}
for stock_code in stock_codes:
    # 获取pe等基础信息
    stock_code_2_indicator[stock_code] = su.stock_individual_indicator(stock_code)
    stock_code_2_history_info[stock_code] = su.stock_daily_history(stock_code, START_DATE, END_DATE)
    stock_code_2_ex_rights[stock_code] = su.stock_individual_ex_rights_detail(stock_code)

    # 没有记录，初始化下
    if stock_code not in stock_code_2_buy_rate:
        stock_code_2_buy_rate[stock_code] = []

    # 没有记录，初始化下
    if stock_code not in stock_code_2_sell_rate:
        stock_code_2_sell_rate[stock_code] = []

    time.sleep(1)


days = du.get_between_days(START_DATE, END_DATE)

# 每天循环
for day in days:
    date = day.date()
    for stock_code in stock_codes:
        # 不存在指标信息，就过滤
        if stock_code not in stock_code_2_indicator:
            continue

        # 不存在历史信息就过滤
        if stock_code not in stock_code_2_history_info:
            continue

        # 获取pe等基础信息
        stock_indicator = stock_code_2_indicator[stock_code]

        # 获取历史每天的信息
        stock_daily_history = stock_code_2_history_info[stock_code]

        # 获取个股所有的除权除息信息
        stock_ex_rights = stock_code_2_ex_rights[stock_code]
        ex_rights_resutl = cu.ex_rights(stock_code, user_account, table, stock_code_2_ex_rights, date)

        date_indicator = stock_indicator[stock_indicator["trade_date"] == date]
        if date_indicator.empty:
            continue

        # 获取PE_TTM
        pe_ttm = date_indicator.get("pe_ttm").item()

        # 估值分位
        percentile = cu.valuation_percentile(stock_indicator, date, "pe_ttm", pe_ttm)

        date_hitory = stock_daily_history[stock_daily_history[const.DATE] == date]
        if date_hitory.empty:
            continue

        # 获取开盘价格
        open_price = date_hitory.get(const.OPEN_PRICE_KEY).item()

        # 小于0的过滤掉
        if open_price <= 0:
            continue

        # 获取当天账户总价值
        total_value = user_account.get_market_value_date(stock_code_2_history_info, date)

        # 单只股票持仓上限金额
        single_limit_cash = total_value / stock_num
        # 股票持仓数量
        stock_holding_num = 0
        if stock_code in user_account.holding_stocks:
            stock_holding_num = user_account.holding_stocks[stock_code].holding_num

        # 单只股票持仓价值
        stock_holding_value = stock_holding_num * open_price

        # 判断买入
        for pe_percentile in BUY_POSITION:
            # 循环，判断买入标准，如果没有满足的，就会直接跳过，直到有满足的，才会走下面的逻辑
            if percentile <= pe_percentile:

                # pe太高的不买
                if pe_ttm > 30:
                    continue

                # 买入比例
                buy_rate = BUY_POSITION[pe_percentile] / 100

                # 股票当前应该持仓上限大于持仓上限10%的，就需要买入，也就是小与30%的就不管了
                diff_rate = buy_rate - stock_holding_value / single_limit_cash
                if diff_rate < 0.1:
                    continue

                # 计算买入金额 持仓比例 * 单只股票上限
                buy_cash = diff_rate * single_limit_cash

                # 确定买入数量
                number = util.can_buy_num(buy_cash, open_price)
                buy_result = user_account.buy(stock_code, open_price, number)
                if buy_result:
                    print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile, "买入金额", number * open_price)
                    stock_holding_num += number

                break
        
        # 可能买入成功了，在计算一次单只股票持仓价值
        stock_holding_value = stock_holding_num * open_price

        for pe_percentile in SELL_POSITION:
            # 没有满这个分位标准，就
            if percentile >= pe_percentile:
                # pe太低的不卖
                if pe_ttm < 40:
                    continue

                sell_rate = SELL_POSITION[pe_percentile] / 100

                diff_rate = stock_holding_value / single_limit_cash - sell_rate
                if diff_rate < 0.5:
                    continue

                # 计算买入金额 持仓比例 * 单只股票上限
                sell_cash = diff_rate * single_limit_cash

                # 确定卖出数量
                number = util.can_buy_num(sell_cash, open_price)
                sell_result = user_account.sell(stock_code, open_price, number)
                if sell_result:
                    print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile, "卖出金额", number * open_price)

                break
    

print("最后交易日开盘的总市值：", total_value)
print(user_account)