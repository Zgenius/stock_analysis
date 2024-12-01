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
START_DATE = "20150101"
END_DATE = datetime.now().strftime("%Y%m%d")

BUY_POSITION = {
    0: 40,
    10: 30,
    20: 20,
    30: 10
}

SELL_POSITION = {
    99: 40,
    90: 30,
    80: 20,
    70: 10
}

BUY_SELL_PAIR = {
    0: 99,
    10: 90,
    20: 80,
    30: 70
}

SELL_BUY_PAIR = dict(zip(BUY_SELL_PAIR.values(), BUY_SELL_PAIR.keys()))

# 选股
# stock_codes = sc.stock_choice()
# print(stock_codes)
# 当天的结果已经有了
stock_codes = [
    "000333",
    "000651",
    "000661",
    "002304",
    "002415",
    "300628",
    "600036",
    "600519",
    "600563",
    "600690",
    "600885",
    "600887",
    "603288",
    "603605",
    "603833",
    "603899"
]

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
for stock_code in stock_codes:
    # 获取pe等基础信息
    stock_code_2_indicator[stock_code] = su.stock_individual_indicator(stock_code)
    stock_code_2_history_info[stock_code] = su.stock_daily_history(stock_code, START_DATE, END_DATE)

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

        # 获取收盘价格
        close_price = date_hitory.get(const.CLOSE_PRICE_KEY).item()

        # 小于0的过滤掉
        if close_price <= 0:
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
        stock_holding_value = stock_holding_num * close_price

        # 判断买入
        for pe_percentile in BUY_POSITION:
            # 循环，判断买入标准，如果没有满足的，就会直接跳过，直到有满足的，才会走下面的逻辑
            if percentile <= pe_percentile:
                # 之前买过并且还没卖，就放弃这个比例的购买，说明买过了
                if pe_percentile in stock_code_2_buy_rate[stock_code] and BUY_SELL_PAIR[pe_percentile] not in stock_code_2_sell_rate[stock_code]:
                    continue

                # pe太高的不买
                if pe_ttm > 30:
                    continue

                # 买入比例
                buy_rate = BUY_POSITION[pe_percentile] / 100

                # 计算买入金额 持仓比例 * 单只股票上限
                buy_cash = buy_rate * single_limit_cash

                print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile)
                # 确定买入数量
                number = util.can_buy_num(buy_cash, close_price)
                user_account.buy(stock_code, close_price, number)
                # 记录这个分位买过了
                stock_code_2_buy_rate[stock_code].append(pe_percentile)
                if BUY_SELL_PAIR[pe_percentile] in stock_code_2_sell_rate[stock_code]:
                    stock_code_2_sell_rate[stock_code].remove(BUY_SELL_PAIR[pe_percentile])
                continue
        
        for pe_percentile in SELL_POSITION:
            # 没有满这个分位标准，就
            if percentile >= pe_percentile:
                # 已经卖出过了或者没有买入，就过滤
                if pe_percentile in stock_code_2_sell_rate[stock_code] or SELL_BUY_PAIR[pe_percentile] not in stock_code_2_buy_rate[stock_code]:
                    continue

                # pe太低的不卖
                if pe_ttm < 10:
                    continue

                sell_rate = SELL_POSITION[pe_percentile] / 100

                # 计算买入金额 持仓比例 * 单只股票上限
                sell_cash = sell_rate * single_limit_cash

                print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile)
                # 确定卖出数量
                number = util.can_buy_num(sell_cash, close_price)
                user_account.sell(stock_code, close_price, number)
                # 记录卖出分位
                stock_code_2_sell_rate[stock_code].append(pe_percentile)
                if SELL_BUY_PAIR[pe_percentile] in stock_code_2_buy_rate[stock_code]:
                    stock_code_2_buy_rate[stock_code].remove(SELL_BUY_PAIR[pe_percentile])
                continue

print(user_account)
# print("网格总盈利： ", table.get_total_profit())
# print("年度盈利: ", table.get_profit_statistics())