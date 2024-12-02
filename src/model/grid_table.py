import utils.calculate_utils as cu

class grid_table:
    # 有效
    STATUS_VALID = 1
    # 无效
    STATUS_INVALID = 2

    # 总记录数
    length = 0
    # 股票代码到交易记录列表
    stock_code_2_records = {}
    # 股票有效的记录数量
    stock_code_2_valid_number = {}
    # 处理过的记录
    handled_records = []
    # 初始化方法
    def __init__(self) -> None:
        self.stock_code_2_records = {}
        self.length = 0
        pass

    # 添加记录
    def add(self, stock):
        # 没有记录，就初始化一次
        if stock.code not in self.stock_code_2_records:
            self.stock_code_2_records[stock.code] = []

        stock_records = self.stock_code_2_records[stock.code]
        # 构造记录
        record = {
            "stock": stock,
            "status": grid_table.STATUS_VALID
        }

        stock_records.append(record)
        self.length += 1

        # 增加有效记录数量
        if stock.code not in self.stock_code_2_valid_number:
            self.stock_code_2_valid_number[stock.code] = 0

        self.stock_code_2_valid_number[stock.code] += 1

    # 移除记录
    def remove(self, stock, index):
        # 清理记录
        del self.stock_code_2_records[stock.code][index]
        if len(self.stock_code_2_records[stock.code]) == 0:
            del self.stock_code_2_records[stock.code]

        self.length -= 1
        self.stock_code_2_valid_number[stock.code] -= 1
        self.handled_records.append(stock)

    # 获取股票网格记录列表
    def get_records(self, stock_code):
        if stock_code not in self.stock_code_2_records:
            return []
        return self.stock_code_2_records[stock_code]

    # 获取持有记录的最小卖出价格
    def get_min_sell_price(self, stock_code, date):
        # 如果没有持仓记录，就返回0，不设定买入价格
        if stock_code not in self.stock_code_2_records:
            return 0
        
        # 获取所有持有网格记录
        records = self.stock_code_2_records[stock_code]
        # 最小买日价格
        min_sell_price = 0
        for record in records:
            # 计算最小买入价格
            sell_price = cu.get_sell_point(record['stock'], date)
            if min_sell_price == 0:
                min_sell_price = sell_price
            else:
                if sell_price < min_sell_price:
                    min_sell_price = sell_price
        
        return min_sell_price
            
    # 获取总盈利
    def get_total_profit(self):
        total_profit = 0
        for record in self.handled_records:
            total_profit += record.profit + record.holding_dividend
        
        return total_profit

    # 获取每年盈利金额
    def get_profit_statistics(self):
        year_2_statistics = {}
        for record in self.handled_records:
            year = record.sell_date.year
            if year not in year_2_statistics:
                year_2_statistics[year] = 0
            
            statistics = year_2_statistics[year]
            statistics += record.profit  + record.holding_dividend
            year_2_statistics[year] = statistics
        
        return year_2_statistics

    # 获取每年盈利金额
    def get_stock_profit_statistics(self):
        year_2_stock_statistics = {}
        for record in self.handled_records:
            year = record.sell_date.year
            if year not in year_2_stock_statistics:
                year_2_stock_statistics[year] = {}
            
            stock_statistics = year_2_stock_statistics[year]
            if record.name not in stock_statistics:
                stock_statistics[record.name] = 0
            
            statistics = stock_statistics[record.name]
            statistics += record.profit
            stock_statistics[record.name] = statistics
            year_2_stock_statistics[year] = stock_statistics
        
        return year_2_stock_statistics