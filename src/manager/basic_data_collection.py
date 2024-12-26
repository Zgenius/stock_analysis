from dao.stock_basic_info import StockBasicInfo
from time import sleep
import utils.stock_utils as su
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc

# 获取所有股票信息
stocks = su.index_contain_stocks(fc.CODE_ZZ_A500)

stock_info_list = []
for stock in stocks.values:
    stock_info = su.stock_individual_info(stock[4])

    stock_record = {
        'symbol': stock[4],
        'name': stock[5],
        'sector': su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_SECTOR),
        'listing_time': su.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY),
        'total_share_capital': su.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_TOTAL_SHARE_CAPITAL),
        'extra_info': "{}"
    }
    stock_info_list.append(stock_record)
    sleep(0.01)

# 批量插入并在冲突时更新
update_fields = ['name', 'sector', 'listing_time', 'total_share_capital', 'extra_info']
StockBasicInfo.batch_create(stock_info_list, update_fields)