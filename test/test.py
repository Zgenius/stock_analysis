from peewee import MySQLDatabase, DatabaseProxy
from dao.stock_basic_info import stock_basic_info
from datetime import datetime

stock_info = stock_basic_info()
stock_info.symbol = "600519"
stock_info.name = "贵州茅台"
stock_info.sector = "食品饮料"
stock_info.listing_time = datetime(2000, 1, 1)
stock_info.total_share_capital = 1200000000
stock_info.extra_info = "{}"

print(stock_info.save())