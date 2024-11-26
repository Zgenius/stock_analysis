from model.stock import stock
from context.market_context import marketContext
import constant.eastmoney_constant as const

class stock_holding(stock):
    # 持有数量
    holding_num = 0
    # 买入价格
    buy_price = 0.0
    # 买入时间
    buy_date = None
    # 盈亏
    profit = 0.0

    # 获取持仓市值
    def getMarketValue(self):
        return self.holding_num * self.getPrice()

    def __str__(self) -> str:
        return "{}({}): 数量{} 价格{}".format(self.name, self.code, str(self.holding_num), self.getPrice())