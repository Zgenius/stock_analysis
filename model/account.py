from model.stock_holding import stock_holding
from context.market_context import marketContext
import constant.eastmoney_constant as const
import datetime

class account:
    # 可用现金
    avilable_cash = 0
    # 持仓股票
    holding_stocks = {}

    def __init__(self, cash):
        self.avilable_cash = cash

    # 账户买入股票
    def buy(self, code, price, number):
        # 判空
        if number == 0 or price <= 0 or code == "":
            return False

        # 买入花销
        cost_amount = price * number
        # 如果县级不够，就直接买入失败
        if cost_amount > self.avilable_cash:
            return False

        if code in self.holding_stocks:
            # 加仓
            buy_stock = self.holding_stocks[code]
            buy_stock.buy_price = (cost_amount + buy_stock.holding_num * buy_stock.buy_price) / (buy_stock.holding_num + number)
            buy_stock.holding_num += number
        else:
            # 建仓
            # 初始化持仓股票
            buy_stock = stock_holding()
            buy_stock.code = code
            buy_stock.name = marketContext.STOCK_CODE_2_INFO[code][const.STOCK_NAME]
            buy_stock.holding_num = number
            buy_stock.buy_price = price
            buy_stock.buy_date = datetime.datetime.now()

        # 减去现金
        self.avilable_cash -= cost_amount
        # 买入成功，账户记录下
        self.holding_stocks[buy_stock.code] = buy_stock

        print("买入成功：{}({}) 价格{} 数量{} 金额{}".format(buy_stock.name, buy_stock.code, price, number, price * number))

        # 买入成功
        return True

    # 账户卖出股票
    def sell(self, code, price, number):
        # 判空
        if number == 0 or price <= 0 or code == "":
            return False

        # 没有持仓，就返回失败
        if code not in self.holding_stocks:
            return False
        
        holding_stock = self.holding_stocks[code]
        # 如果卖出的数量大于持仓数量，就返回失败，无法卖出
        if holding_stock.holding_num < number:
            return False
        
        # 卖出之后，剩余持仓
        holding_stock.holding_num -= number
        # 股票卖出，增加现金
        self.avilable_cash += price * number

        # 如果还有持仓，更新下数据
        if holding_stock.holding_num != 0:
            self.holding_stocks[code] = holding_stock
        else:
            # 如果已经清仓了，就删除这个持仓
            del self.holding_stocks[code]

        print("卖出成功：{}({}) 价格{} 数量{} 金额{}".format(holding_stock.name, holding_stock.code, price, number, price * number))
        
        return True
    
    # 获取总资产
    def get_total_asset(self):
        return self.get_market_value() + self.avilable_cash

    # 获取总市值
    def get_market_value(self):
        market_value = 0.0
        for index in self.holding_stocks:
            stock = self.holding_stocks[index]
            market_value += stock.getMarketValue()

        return market_value

    def __str__(self) -> str:
        template = "总资产: {}\n市值: {}\n可用现金: {}\n持仓股票: \n".format(self.get_total_asset(), self.get_market_value(), self.avilable_cash)
        holding = ""
        for index in self.holding_stocks:
            holding += str(self.holding_stocks[index]) + "\n"
        
        return template + holding
        