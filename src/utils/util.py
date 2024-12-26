import re

# 获取可以购买的数量
def can_buy_num(cash, price):
    if cash == 0 or price == 0:
        return 0
    
    return (cash // (price * 100)) * 100

# 字典拆包
def unpack_dict(data):
    return tuple(data.values())

# 通过固定长度分组列表
def group_list_by_fixed_length(lst, group_size):
    groups = []
    for i in range(0, len(lst), group_size):
        groups.append(lst[i:i + group_size])
    return groups

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()