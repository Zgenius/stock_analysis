from model.stock_basic_info import StockBasicInfo
from model.stock_px_brief import StockPxBrief
from model.stock_price_history_daily import StockPriceHistoryDaily
from model.account import account
from utils.util import group_list_by_fixed_length
from datetime import datetime
from sqlalchemy import and_
from datetime import datetime, timedelta
import utils.util as util
import utils.date_utils as du
import math
import json
import os

'''
沃尔特施洛斯的烟蒂股策略数字化
不深研, 全凭统计学
买入策略
    1.低pe: 低于15
    2.低pb: 低于0.67
    3.低price: 3年股价最低位置附近, 理论上不超过最低点20%
    4.低负债: 负债率50%就不要碰了
持仓策略
    1.分散持仓, 个股仓位不超过5%
    2.每天计算是否涨幅超过50%
    3.每天计算所有买入超过1年的股票是否满足标准, 不满足就换称符合标准的
卖出策略
    1.涨幅超过50%, 卖出50%仓位
'''

class walterSchloss:
    # 时间范围
    START_DATE = "20140101"
    END_DATE = datetime.now().strftime("%Y%m%d")

    user_account = account(1000000)

    def run(self):
        days = du.get_between_days(self.START_DATE, self.END_DATE)
        config_path = f"data/data_{self.END_DATE}.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                date2_symbols = json.load(f)
        
            date_2_satisfied_symbols = {}
            for date, symbols in date2_symbols.items():
                date_2_satisfied_symbols[datetime.strptime(date, "%Y%m%d")] = symbols
        else:
            date_2_satisfied_symbols = self.choice(days)
            with open(config_path, 'w') as f:
                json.dump(date_2_satisfied_symbols, f)

        # config_path = 'data/data.json'
        # with open(config_path, 'r') as f:
        #     date2_symbols = json.load(f)
        
        # date_2_satisfied_symbols = {}
        # for date, symbols in date2_symbols.items():
        #     date_2_satisfied_symbols[datetime.strptime(date, "%Y%m%d")] = symbols

        for day in days:
            if day not in date_2_satisfied_symbols:
                continue

            satisfied_symbols = date_2_satisfied_symbols[day]
            # 获取最新交易日
            self.trade_date = day
            symbol_length = len(satisfied_symbols)
            if len(satisfied_symbols) == 0:
                continue

            self.buy(satisfied_symbols)
            self.sell(satisfied_symbols)

        print(self.user_account)
        return
    
    def buy(self, symbols):
        if symbols == None or len(symbols) == 0:
            return
        
        user_account = self.user_account
        price_history = StockPriceHistoryDaily.select(StockPriceHistoryDaily).where(and_(StockPriceHistoryDaily.symbol.in_(symbols), StockPriceHistoryDaily.trade_date == self.trade_date)).order_by(StockPriceHistoryDaily.trade_date.desc()).all()
        if len(price_history) == 0:
            return
        
        symbol_2_price_info = {}
        for price_info in price_history:
            symbol_2_price_info[price_info.symbol] = price_info
        
        symbol_length = len(symbols)
        total_asset = user_account.get_total_asset(self.trade_date)
        # 单只上限是5%
        single_stock_limit = math.floor(total_asset / min(symbol_length, 20))
        for symbol in symbols:
            if symbol not in symbol_2_price_info:
                continue

            price = symbol_2_price_info[symbol].closing_price
            number = util.can_buy_num(single_stock_limit, price)
            self.user_account.buy(symbol, price, number, self.trade_date)

    
    def sell(self, symbols):
        if len(self.user_account.holding_stocks) == 0:
            return
        
        hold_symbols = self.user_account.holding_stocks.keys()
        price_history = StockPriceHistoryDaily.select(StockPriceHistoryDaily).where(and_(StockPriceHistoryDaily.symbol.in_(hold_symbols), StockPriceHistoryDaily.trade_date == self.trade_date)).order_by(StockPriceHistoryDaily.trade_date.desc()).all()

        symbol_2_price_info = {}
        for price_info in price_history:
            symbol_2_price_info[price_info.symbol] = price_info

        holding_stocks = self.user_account.holding_stocks.copy()
        for symbol, stock in holding_stocks.items():
            if symbol not in symbol_2_price_info:
                continue

            price = symbol_2_price_info[symbol].closing_price
            if price / stock.buy_price <= 1.5 or symbol not in symbols:
                continue

            self.user_account.sell(symbol, price, stock.holding_num)
    
    def choice(self, dates):
        satisfied_symbols = []
        # 获取所有报告摘要
        stocks = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()
        # 将stocks列表按照每组100个进行分组
        date_chunks = group_list_by_fixed_length(dates, 100)
        date_2_satisfied_symbols = {}
        for date_chunk in date_chunks:
            satisfied_symbol_chunk = self.choice_chunk(stocks, date_chunk)
            date_2_satisfied_symbols.update(satisfied_symbol_chunk)
        
        return date_2_satisfied_symbols

    def filter_pe_and_pb(self, symbols, dates) -> dict:
        if symbols == None or len(symbols) == 0:
            return {}
        
        where = and_(
            StockPxBrief.symbol.in_(symbols), 
            StockPxBrief.trade_date.in_(dates),
            StockPxBrief.pe_ttm > 0.0,
            StockPxBrief.pe_ttm <= 15,
            StockPxBrief.pb < 1
        )
        
        # 查询满足pe_ttm<=15 and pb < 1的股票
        px_briefs = StockPxBrief.select(StockPxBrief.symbol, StockPxBrief.trade_date).where(where).all()
        if px_briefs is None or len(px_briefs) == 0:
            return {}
        
        date_2_symbols = {}
        for px_brief in px_briefs:
            if px_brief.trade_date not in date_2_symbols:
                date_2_symbols[px_brief.trade_date] = []
            
            date_2_symbols[px_brief.trade_date].append(px_brief.symbol)

        return date_2_symbols

    def filter_price(self, date_2_symbols, dates) -> dict:
        if date_2_symbols == None or len(date_2_symbols) == 0 or dates == None:
            return []

        symbols = []
        for symbol_chunk in date_2_symbols.values():
            symbols.extend(symbol_chunk)
            symbols = list(set(symbols))


        min_date = min(dates)
        max_date = max(dates)
        year3ago = min_date - timedelta(days = 365 * 3)

        date_2_satisfied_symbols = {}
        symbol_chunks = group_list_by_fixed_length(symbols, 5)
        for symbol_chunk in symbol_chunks:
            where = and_(
                StockPriceHistoryDaily.symbol.in_(symbol_chunk), 
                StockPriceHistoryDaily.trade_date.between(year3ago, max_date)
            )

            price_history = StockPriceHistoryDaily.select(StockPriceHistoryDaily).where(where).order_by(StockPriceHistoryDaily.trade_date.desc()).all()
            if price_history == None or len(price_history) == 0:
                continue

            symbol_2_date_2_price_info = {}
            for price_info in price_history:
                if price_info.symbol not in symbol_2_date_2_price_info:
                    symbol_2_date_2_price_info[price_info.symbol] = {}
                
                symbol_2_date_2_price_info[price_info.symbol][price_info.trade_date] = price_info
        
            for date in dates:
                start_date = date - timedelta(days = 365 * 3)
                for symbol, date_2_price_info in symbol_2_date_2_price_info.items():
                    if date not in date_2_price_info:
                        continue

                    # 当天的价格信息
                    price_info = date_2_price_info[date]
                    price_info_list = []
                    for trade_date, price_item in date_2_price_info.items():
                        if trade_date < start_date or trade_date > date:
                            continue
                        price_info_list.append(price_item)
                    
                    price_list = [price.closing_price for price in price_info_list]
                    low_price = min(price_list)
                    # 最近3年内，从最低价格上涨超过20%的过滤掉
                    if price_info.closing_price / low_price > 1.2:
                        continue

                    if date not in date_2_satisfied_symbols:
                        date_2_satisfied_symbols[date] = []
                    
                    date_2_satisfied_symbols[date].append(symbol)

        return date_2_satisfied_symbols

    
    def choice_chunk(self, stocks, dates) -> dict:
        if stocks is None or len(stocks) == 0 or dates is None:
            return []
        
        # 获取所有股票代码
        symbols = [stock.symbol for stock in stocks]
        date_2_symbols = self.filter_pe_and_pb(symbols, dates)
        date_2_symbols = self.filter_price(date_2_symbols, dates)

        return date_2_symbols


if __name__ == "__main__":
    walterSchloss().run()
    print("walter_schloss.py done")