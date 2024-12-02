from model.stock import stock
from context.market_context import market_context
import constant.eastmoney_constant as const

class stock_holding(stock):
    # 持有数量
    holding_num = 0
    # 买入价格
    buy_price = 0.0
    # 买入时间
    buy_date = None
    # 卖出价格
    sell_price = 0.0
    # 卖出时间
    sell_date = None
    # 盈亏
    profit = 0.0
    # 持仓红利
    holding_dividend = 0.0

    # 获取持仓市值
    def getMarketValue(self):
        return self.holding_num * self.getPrice()
        
    # 输出格式化字符串
    def __str__(self) -> str:
        return "{}({}): 数量{} 价格{}".format(self.name, self.code, str(self.holding_num), self.getPrice())