import constant.eastmoney_constant as const
from model.transacation_cost import transacation_cost
from model.stock_holding import stock_holding
from context.market_context import market_context
from datetime import datetime

class account:
    # 最小单位
    MIN_NUMBER = 100
    # 可用现金
    availible_cash = 0
    # 持仓股票
    holding_stocks = {}

    transacation = transacation_cost()

    def __init__(self, cash):
        self.availible_cash = cash
        self.holding_stocks = {}

    # 账户买入股票
    def buy(self, code, price, number, date = datetime.now()):
        # 判空
        if number == 0 or price <= 0 or code == "":
            return False

        # 必须是100的整数倍
        if number % self.MIN_NUMBER != 0:
            return False

        # 买入花销
        cost_amount = price * number + self.transacation.compute_buy_cost(price, number)
        # 如果县级不够，就直接买入失败
        if cost_amount > self.availible_cash:
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
            buy_stock.name = market_context.STOCK_CODE_2_INFO[code][const.STOCK_NAME]
            buy_stock.holding_num = number
            buy_stock.buy_price = cost_amount / number
            buy_stock.buy_date = date

        # 减去现金
        self.availible_cash -= cost_amount
        # 买入成功，账户记录下
        self.holding_stocks[buy_stock.code] = buy_stock

        print("买入成功：{}({}) 价格{} 数量{} 金额{}".format(buy_stock.name, buy_stock.code, cost_amount / number, number, cost_amount))

        # 买入成功
        return True

    # 账户卖出股票
    def sell(self, code, price, number):
        # 判空
        if number == 0 or price <= 0 or code == "":
            return False
        
        # 必须是100的整数倍
        # if number % self.MIN_NUMBER != 0:
        #     return False

        # 没有持仓，就返回失败
        if code not in self.holding_stocks:
            return False
        
        holding_stock = self.holding_stocks[code]
        # 如果卖出的数量大于持仓数量，就返回失败，无法卖出
        if holding_stock.holding_num < number:
            return False
        
        # 卖出现金
        sell_cash = price * number - self.transacation.compute_sell_cost(price, number)
       
        # 卖出之后，剩余持仓
        holding_stock.holding_num -= number
        # 股票卖出，增加现金
        self.availible_cash += sell_cash

        # 如果还有持仓，更新下数据
        if holding_stock.holding_num != 0:
            self.holding_stocks[code] = holding_stock
        else:
            # 如果已经清仓了，就删除这个持仓
            del self.holding_stocks[code]

        print("卖出成功：{}({}) 价格{} 数量{} 金额{}".format(holding_stock.name, holding_stock.code, price, number, sell_cash))
        
        return True
    
    # 获取总资产
    def get_total_asset(self):
        return self.get_market_value() + self.availible_cash

    # 获取总市值
    def get_market_value(self):
        market_value = 0.0
        for index in self.holding_stocks:
            stock = self.holding_stocks[index]
            market_value += stock.getMarketValue()

        return market_value

    def __str__(self) -> str:
        template = "总资产: {}\n市值: {}\n可用现金: {}\n持仓股票: \n".format(self.get_total_asset(), self.get_market_value(), self.availible_cash)
        holding = ""
        for index in self.holding_stocks:
            holding += str(self.holding_stocks[index]) + "\n"
        
        return template + holding
        
    # 获取某个日期的总市值
    def get_market_value_date(self, stock_code_2_history_info, date):
        market_value = 0.0
        for index in self.holding_stocks:
            stock = self.holding_stocks[index]
            stock_history_info = stock_code_2_history_info[index]
            date_hitory = stock_history_info[stock_history_info[const.DATE] == date]
            if date_hitory.empty:
                continue

            # 获取收盘价格
            close_price = date_hitory.get(const.CLOSE_PRICE_KEY).item()

            market_value += close_price * stock.holding_num

        return market_value + self.availible_cash

    # 获取持仓占比
    def stock_percentage(self, stock_code, stock_code_2_history_info, date):
        total_value = self.get_market_value_date(stock_code_2_history_info, date)
        stock_history_info = stock_code_2_history_info[stock_code]
        date_hitory = stock_history_info[stock_history_info[const.DATE] == date]
        if date_hitory.empty:
            return 0

        # 获取收盘价格
        close_price = date_hitory.get(const.CLOSE_PRICE_KEY).item()
        stock = self.holding_stocks[stock_code]

        return close_price * stock.holding_num / total_value