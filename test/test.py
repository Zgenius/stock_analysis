import cair_stock as cs
import constant.eastmoney_constant as const
import strategy.MeanReversionStrategyBaseResiduals as mr
import sys
from datetime import datetime
from model.account import account
from model.stock_holding import stock_holding


# stock_holding_1 = stock_holding()
# print(stock_holding_1)

# 初始化账户
user_account = account(10000)
user_account.buy("000001", 10, 100)
user_account.sell("000001", 20, 50)
print(user_account)