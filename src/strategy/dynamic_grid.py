import manager.stock_choice as sc
import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import utils.util as util
import copy
import utils.date_utils as du
import time
from model.account import account
from datetime import datetime
from model.grid_table import grid_table

"""
动态网格策略回测
"""

# 通过字符串或者int获取datetime对象
def get_date(dateStr):
    if type(dateStr) == str:
        date = datetime.strptime(dateStr, "%Y%m%d")
    elif type(dateStr) == int:
        date = datetime.strptime(str(dateStr), "%Y%m%d")
    else:
        date = dateStr
    return date

# 时间范围
START_DATE = "20220101"
END_DATE = datetime.now().strftime("%Y%m%d")

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

# 初始化账户
user_account = account(1000000)
print(user_account)

# 初始化网格记录表
table = grid_table()

# 记录股票编码到指标类信息的映射
stock_code_2_indicator = {}
# 股票编码到历史数据的映射表
stock_code_2_history_info = {}
for stock_code in stock_codes:
    # 获取pe等基础信息
    stock_code_2_indicator[stock_code] = su.stock_individual_indicator(stock_code)
    stock_code_2_history_info[stock_code] = su.stock_daily_history(stock_code, START_DATE, END_DATE)
    time.sleep(1)

days = du.get_between_days(START_DATE, END_DATE)
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

        total_value = user_account.get_market_value_date(stock_code_2_history_info, date)
        # 确定买入数量，第一次建仓买入不超过2%总资产
        number = util.can_buy_num(total_value / 50, close_price)

        # 没有持仓，并且估值分位小于70%，就买入第一笔
        if stock_code not in table.stock_code_2_records and percentile < 70:
            buy_result = user_account.buy(stock_code, close_price, number, date)
            if not buy_result:
                continue
            print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile)
            stock = copy.deepcopy(user_account.holding_stocks[stock_code])
            stock.buy_price = close_price
            stock.buy_date = date
            # 网格表记录
            table.add(stock)

            continue

        grid_records = table.get_records(stock_code)
        for grid_record_key, grid_record in enumerate(grid_records):
            # 获取卖点价格
            sell_price = cu.get_sell_point(grid_record['stock'], date)
            if close_price >= sell_price:
                # 满足卖点，卖出
                sell_result = user_account.sell(stock_code, close_price, grid_record['stock'].holding_num)
                if not sell_price:
                    continue
                print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile)
                stock = copy.deepcopy(grid_record['stock'])
                stock.sell_price = close_price
                stock.sell_date = date
                stock.profit = (close_price - stock.buy_price) * stock.holding_num
                # 卖出之后，记录卖出信息
                table.remove(stock, grid_record_key)
                continue
            else:
                # 获取买点，持仓里面最小卖出价格的92.5%
                min_sell_price = table.get_min_sell_price(stock_code, date)
                # 如果没有持仓了，返回0，股价不可能小于0，所以这里的条件无法出发，不会买入
                buy_price = min_sell_price * 0.925
                stock_percentage = (user_account.holding_stocks[stock_code].holding_num * close_price) / total_value
                if close_price <= buy_price and percentile < 70 and stock_percentage < 0.1:
                    buy_result = user_account.buy(stock_code, close_price, number)
                    if not buy_result:
                        continue
                    print("日期：", date, "pe_ttm: ", pe_ttm, "分位: ", percentile)
                    stock = copy.deepcopy(user_account.holding_stocks[stock_code])
                    stock.buy_price = close_price
                    stock.buy_date = date
                    stock.holding_num = number

                    table.add(stock)
                    continue

print(user_account)
print("网格总盈利： ", table.get_total_profit())
print("年度盈利: ", table.get_profit_statistics())
print("年度个股盈利: ", table.get_stock_profit_statistics())
exit(0)