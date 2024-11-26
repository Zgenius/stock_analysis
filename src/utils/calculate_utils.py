import numpy as np
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