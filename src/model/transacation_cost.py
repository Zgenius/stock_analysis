# 交费用类，在买入和卖出的时候需要扣除
class transacation_cost:
    '''
    券商交易佣金
        定义: 佣金是投资者通过证券公司进行股票交易时支付给证券公司的服务费用
        收取方式: 买入和卖出股票时均需支付佣金
        税率: 
            最高标准: 佣金最高不超过成交金额的0.3%
            最低标准: 单笔交易佣金不满5元按5元收取
    '''
    BROKERAGE_COMMISSION_RATE = 0.003
    '''
    印花税
        定义：印花税是投资者在卖出股票时支付给财税部门的税收
        收取方式：仅在卖出股票时收取，买入时不收取
        税率: 成交金额的0.1%
    '''
    STAMP_DUTY_RATE = 0.001
    '''
    过户费
        定义: 过户费是股票成交后，更换户名所需支付的费用
        收取方式: 买入和卖出股票时均需支付过户费
        费率: 成交金额的0.01%
    '''
    TRANSFER_FEE_RATE = 0.0001
    '''
    证管费
        定义：支付给中国证券监督管理委员会的费用
        收取方式: 买入和卖出股票时均需支付证管费
        收费标准: 成交金额的0.002%
    '''
    CERTIFICATE_MANAGEMENT_FEE_RATE = 0.00002
    '''
    证券交易经手费
        定义: 支付给证券交易所的费用
        收取方式: 买入和卖出股票时均需支付证券交易经手费
        收费标准: 成交金额的0.00341%(沪深交易所), 成交金额的0.0125%(北交所)
    '''
    SECURITIES_TRADING_HANDLING_FEE_RATE = 0.0000341

    # 计算券商佣金收取
    def compute_commission_cost(self, price, number):
        commission = price * number * self.BROKERAGE_COMMISSION_RATE
        # 如果佣金小于5，就按照5元
        if commission < 5:
            commission = 5
        
        return commission
    
    # 计算印花税
    def compute_stamp_duty(self, price, number):
        return price * number * self.STAMP_DUTY_RATE
    
    # 过户费
    def compute_transfer_free(self, price, number):
        return price * number * self.TRANSFER_FEE_RATE
    
    # 证管费
    def compute_certificate_management_fee(self, price, number):
        return price * number * self.CERTIFICATE_MANAGEMENT_FEE_RATE
    
    # 证券交易经手费
    def compute_securities_trading_handling_fee(self, price, number):
        return price * number * self.SECURITIES_TRADING_HANDLING_FEE_RATE

    # 买入花销
    def compute_buy_cost(self, price, number):
        cost = 0.0
        cost += self.compute_commission_cost(price, number)
        cost += self.compute_transfer_free(price, number)
        cost += self.compute_certificate_management_fee(price, number)
        cost += self.compute_securities_trading_handling_fee(price, number)
        
        return cost
    
    # 卖出花销
    def compute_sell_cost(self, price, number):
        cost = 0.0
        cost += self.compute_commission_cost(price, number)
        cost += self.compute_transfer_free(price, number)
        cost += self.compute_certificate_management_fee(price, number)
        cost += self.compute_securities_trading_handling_fee(price, number)
        cost += self.compute_stamp_duty(price, number)

        return cost