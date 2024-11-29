import numpy as np
import math
from datetime import datetime
 
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