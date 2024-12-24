# 获取可以购买的数量
def can_buy_num(cash, price):
    if cash == 0 or price == 0:
        return 0
    
    return (cash // (price * 100)) * 100

# 字典拆包
def unpack_dict(data):
    return tuple(data.values())