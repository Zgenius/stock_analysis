import numpy as np
import math
from datetime import timedelta
 
# 计算给定列表的标准差
def calculate_std_dev(numbers):
    mean = np.mean(numbers)
    std_dev = np.sqrt(np.mean((numbers - mean) ** 2))
    return std_dev

# 计算列表的差集
def calculate_difference_set(list_a, list_b):
    return list(set(list_a) - set(list_b))

# 计算列表交集
def calculate_intersection_set(list_a, list_b):
    return list(set(list_a) & set(list_b))

# 获取卖点
def get_sell_point(stock, date):
    if stock.code == "":
        return 0.0
    
    # 每年28%的收益率,每个月的收益率
    ideal_profit_rate_month = 0.28 / 12
    # 买入时间到输入时间一共经历多少天
    delta = (date - stock.buy_date).days

    # 获取向上取整的月份数
    month_number = math.ceil(delta / 30)
    if month_number == 0:
        month_number = 1

    return (month_number * ideal_profit_rate_month + 1) * stock.buy_price


# 获取卖点精确
def get_sell_point_v2(stock, date):
    if stock.code == "":
        return 0.0
    
    # 每年28%的收益率,每个月的收益率
    ideal_profit_rate_day = 0.28 / 365
    # 买入时间到输入时间一共经历多少天
    delta = (date - stock.buy_date).days
    # 如果时间小于1个月，算一个月
    if delta < 30:
        delta = 30

    return (delta * ideal_profit_rate_day + 1) * stock.buy_price

# 计算估值分位
def valuation_percentile(indicator, date, key, value):
    start_date = date - timedelta(days = 365 * 5)
    indicator_data = indicator[indicator["trade_date"] >= start_date]
    indicator_data = indicator_data[indicator_data["trade_date"] <= date]
    # 获取范围内估值指标所有的数据列表
    valuation_list = indicator_data.get(key)

    min = valuation_list.min()
    max = valuation_list.max()

    if min <= 0:
        min = 0
    
    if max <= 0:
        max = 0
    
    if max - min == 0:
        return 100
    
    # 计算估值百分位
    return (value - min) / (max - min) * 100

# 除权除息
def ex_rights(stock_code, user_account, grid_table, ex_right_info, date):
    if stock_code not in ex_right_info:
        return False

    # 没有持仓，就返回
    if stock_code not in user_account.holding_stocks:
        return False

    ex_rights = ex_right_info[stock_code]
    ex_right = ex_rights[ex_rights["除权除息日"] == date]
    # 当天没有除权除息，就啥也不干
    if ex_right.size == 0:
        return False
    
    # 单位是每10股分多少，计算成每股分多少
    cash_dividend = ex_right.get("现金分红-现金分红比例").item()
    # 如果不是nan，就说明有分红，处理分红除权
    if not math.isnan(cash_dividend):
        cash_dividend = cash_dividend / 10
        # 持仓账户处理，有持仓，这时候要吧持仓股票进行除权
        if stock_code in user_account.holding_stocks:
            stock = user_account.holding_stocks[stock_code]
            # 持仓股价-每股分红
            stock.buy_price -= cash_dividend
            user_account.holding_stocks[stock_code] = stock
            # 分红增加到现金上
            user_account.availible_cash += stock.holding_num * cash_dividend
            print("{}({})".format(stock.name, stock.code), "分红除权，每股现金: ", cash_dividend)
        
        # 网格交易表存在持仓，进行除权处理
        if stock_code in grid_table.stock_code_2_records:
            # 拿出来所有网格持仓信息的记录
            records = grid_table.stock_code_2_records[stock_code]
            for index, record in enumerate(records):
                # 买入价格减去现金分红
                record['stock'].buy_price -= cash_dividend
                # 记录持仓红利
                record['stock'].holding_dividend += cash_dividend * record['stock'].holding_num
                grid_table.stock_code_2_records[stock_code][index] = record
    
    # 配股，每个单位是10股
    right_issue = ex_right.get("送转股份-转股比例").item()
    if not math.isnan(right_issue):
        # 每股配股多少份
        right_issue = right_issue / 10
        # 配股比例，每股配股数额 + 1
        right_issue_rate = right_issue + 1
        if stock_code in user_account.holding_stocks:
            stock = user_account.holding_stocks[stock_code]
            # 股价除权
            stock.buy_price = stock.buy_price / right_issue_rate
            # 股票数量更新
            stock.holding_num = stock.holding_num * right_issue_rate
            # 更新进持仓
            user_account.holding_stocks[stock_code] = stock
            print("{}({})".format(stock.name, stock.code), "配股除权，每股配股: ", right_issue)

        # 网格交易表存在持仓，进行除权处理
        if stock_code in grid_table.stock_code_2_records:
            # 拿出来所有网格持仓信息的记录
            records = grid_table.stock_code_2_records[stock_code]
            for index, record in enumerate(records):
                # 股价变化了
                record['stock'].buy_price = record['stock'].buy_price / right_issue_rate
                record['stock'].holding_num = record['stock'].holding_num * right_issue_rate
                # 更新进网格
                grid_table.stock_code_2_records[stock_code][index] = record

    return True

# 按照字典值排序
def dict_sort(data):
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

# 计算指标平均值，输入参数stock_code -> date -> indicator
def stock_code_2_avg(stock_code_2_date_indicator):
    stock_code_2_avg_indicator = {}
    for stock_code, date_2_indicator in stock_code_2_date_indicator.items():
        total_ROE = 0
        for indicator in date_2_indicator.values():
            # 过滤掉ROE，ROE是nan的在亏损
            if math.isnan(indicator):
                continue
            # ROE汇总
            total_ROE += indicator

        total_len = len(date_2_indicator)

        if total_len == 0:
            stock_code_2_avg_indicator[stock_code] = 0
        else:
            stock_code_2_avg_indicator[stock_code] = total_ROE / total_len
    
    return stock_code_2_avg_indicator

# 获取指标最大值
def indicator_max(indicator, date, key):
    start_date = date - timedelta(days = 365 * 10)
    indicator_data = indicator[indicator["trade_date"] >= start_date]
    indicator_data = indicator_data[indicator_data["trade_date"] <= date]
    # 获取范围内估值指标所有的数据列表
    valuation_list = indicator_data.get(key)

    max = valuation_list.max()

    if max > 50:
        max = 50

    return max