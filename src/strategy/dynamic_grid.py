import manager.stock_choice as sc
import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import utils.util as util
import copy
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
START_DATE = "20160101"
END_DATE = datetime.now().strftime("%Y%m%d")

# 选股
# stock_codes = sc.stock_choice()
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

for stock_code in stock_codes:
    # 获取pe等基础信息
    stock_indicator = su.stock_individual_indicator(stock_code)

    # 初始化账户
    user_account = account(1000000)
    print(user_account)

    # 动态网格记录
    grid_records = []
    # 初始化网格记录表
    table = grid_table()

    # 获取历史每天的信息
    stock_daily_history = su.stock_daily_history(stock_code, START_DATE, END_DATE)
    for index, stock_daily_info in stock_daily_history.iterrows():
        # 日期
        date = get_date(stock_daily_info[const.DATE])

        pe_ttm = stock_indicator[stock_indicator["trade_date"] == date].get("pe_ttm").item()
        # if pe_ttm > 15:
        #     continue
        # 估值分位
        percentile = cu.valuation_percentile(stock_indicator, date, "pe_ttm", pe_ttm)

        # 价格
        close_price = stock_daily_info[const.CLOSE_PRICE_KEY]
        # 涨跌幅，过大，说明数据有问题
        if stock_daily_info["涨跌幅"] > 15:
            continue

        # 小于0的过滤掉
        if close_price <= 0:
            continue

        cash = user_account.avilable_cash
        if stock_code in user_account.holding_stocks:
            cash += user_account.holding_stocks[stock_code].holding_num * close_price

        # 确定买入数量，第一次建仓买入十分之一
        number = util.can_buy_num(cash / 50, close_price)

        # 首次买入
        if table.length == 0 and percentile < 70:
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
                if close_price <= buy_price and percentile < 70:
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
    exit(0)