from dao.stock_basic_info import StockBasicInfo
from datetime import datetime
import utils.stock_utils as su
import constant.fund_code_constant as fc
import constant.eastmoney_constant as const
from time import sleep

# 所有股票信息
stocks = su.index_contain_stocks(fc.CODE_ZZ_500)

exist_stock_basic_info_list = StockBasicInfo.select(StockBasicInfo.symbol)
exist_symbols = []
for exist_stock_info in exist_stock_basic_info_list:
    exist_symbols.append(exist_stock_info.symbol)

stock_info_list = []
for stock in stocks.values:
    if stock[4] in exist_symbols:
        continue

    stock_info = su.stock_individual_info(stock[4])

    stock_record = StockBasicInfo()
    stock_record.symbol = stock[4]
    stock_record.name = stock[5]
    stock_record.sector = su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_SECTOR)
    stock_record.listing_time = su.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY)
    stock_record.total_share_capital = su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_TOTAL_SHARE_CAPITAL)
    stock_record.extra_info = "{}"
    stock_info_list.append(stock_record)
    sleep(0.01)

StockBasicInfo.bulk_create(stock_info_list)