import constant.eastmoney_constant as const
from context.market_context import marketContext

class stock:
    # 股票代码
    code = ""
    # 股票名称
    name = ""
    # 价格
    price = 0.0

    # 获取当前最新价
    def getPrice(self):
        if self.code == "":
            return self.price

        return marketContext.STOCK_CODE_2_INFO[self.code][const.STOCK_PRICE]