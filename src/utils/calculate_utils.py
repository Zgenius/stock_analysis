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