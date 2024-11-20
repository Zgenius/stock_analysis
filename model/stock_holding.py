from model.stock import stock

class stock_holding(stock):
    # 持有数量
    holding_num = 0
    # 买入价格
    buy_price = 0.0
    # 买入时间
    buy_date = None
    # 盈亏
    profit = 0.0

    def __str__(self) -> str:
        return self.code + ": " + str(self.holding_num)