import utils.calculate_utils as cc
import constant.eastmoney_constant as const
import akshare as ak

# 获取沪深京A股列表
def stock_list(): 
    return ak.stock_zh_a_spot_em()


# 去掉不一致的日期数据
def sync_data_list(stocks_a, stocks_b):
    # 只有都存在的日期才可以进行计算
    intersection_date_set = cc.calculate_intersection_set(stocks_a[const.DATE], stocks_b[const.DATE])

    stocks_intersection_a = filter_data(stocks_a, intersection_date_set)
    stocks_intersection_b = filter_data(stocks_b, intersection_date_set)

    return [stocks_intersection_a, stocks_intersection_b]

# 过滤数据
def filter_data(stocks, intersection_date_set):
    return stocks[stocks[const.DATE].isin(intersection_date_set)].reset_index(drop=True)

# 获取股票编码到信息的字典
def stock_code_2_info():
    stocks = stock_list()
    stock_code_2_info = {}
    for index, row in stocks.iterrows():
        stock_code_2_info[row[const.STOCK_CODE]] = row
    return stock_code_2_info

# 获取指数列表
def index_list(symbol_name = "指数成份"):
    return ak.stock_zh_index_spot_em(symbol=symbol_name)

# 获取指数成分
def index_contain_stocks(symbol_code = "00300"):
    return ak.index_stock_cons_csindex(symbol=symbol_code)

# 获取股票历史每天数据
def stock_daily_history(symbol_code, start_date, end_date):
    return ak.stock_zh_a_hist(symbol=symbol_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
