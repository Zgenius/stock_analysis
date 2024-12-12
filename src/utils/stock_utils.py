import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import akshare as ak
import time
from datetime import datetime

# 获取沪深京A股列表
def stock_list(): 
    return ak.stock_zh_a_spot_em()

# 去掉不一致的日期数据
def sync_data_list(stocks_a, stocks_b):
    # 只有都存在的日期才可以进行计算
    intersection_date_set = cu.calculate_intersection_set(stocks_a[const.DATE], stocks_b[const.DATE])

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

# 获取股票某个季度的基本面信息
def stock_code_2_base_info(date):
    base_info = ak.stock_yjbb_em(date)
    stock_code_2_base_info = {}
    for index, row in base_info.iterrows():
        stock_code_2_base_info[row[const.STOCK_INDIVIDUAL_CODE]] = row
    return stock_code_2_base_info

# 获取指数列表
def index_list(symbol_name = "指数成份"):
    return ak.stock_zh_index_spot_em(symbol=symbol_name)

# 获取指数成分
def index_contain_stocks(symbol_code = "00300"):
    return ak.index_stock_cons_csindex(symbol=symbol_code)

# 获取股票历史每天数据
def stock_daily_history(symbol_code, start_date, end_date):
    # return ak.stock_zh_a_hist(symbol=symbol_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    # return ak.stock_zh_a_hist(symbol=symbol_code, period="daily", start_date=start_date, end_date=end_date, adjust="hfq")
    return ak.stock_zh_a_hist(symbol=symbol_code, period="daily", start_date=start_date, end_date=end_date)

# 获取个股的基础信息
# 包括： 总市值，流通市值，行业，上市时间，股票代码，股票简称，总股本，流通股
def stock_individual_info(symbol):
    return ak.stock_individual_info_em(symbol)

# 获取个股的一些财务指标
# 包括： pe pe_ttm pb ps ps_ttm dv_ratio dv_ttm total_mv
def stock_individual_indicator(symbol):
    return ak.stock_a_indicator_lg(symbol)

# 获取个股的基本信息的一个字段
def stock_individual_info_get(stock_info, key):
    return stock_info[stock_info["item"].eq(key)]["value"].iloc[0]

# 获取每只股票的除权派息信息
def stock_individual_ex_rights_detail(symbol):
    return ak.stock_fhps_detail_em(symbol)

# 获取股票的财务基本信息
def stock_2_date_base_info(date_list):
    # 循环查询每个日期的净资产收益率
    stock_code_2_date_2_base_info = {}
    for date in date_list:
        # 获取每个财报日的基础信息
        stock_code_2_info = stock_code_2_base_info(date)
        for stock_code, base_info in stock_code_2_info.items():
            # 如果还没有赋值过，就初始化赋值
            if stock_code not in stock_code_2_date_2_base_info:
                stock_code_2_date_2_base_info[stock_code] = {}
            
            # 按到日期到基础信息的字典
            date_2_base_info = stock_code_2_date_2_base_info[stock_code]
            date_2_base_info[date] = base_info
            # 数据写入
            stock_code_2_date_2_base_info[stock_code] = date_2_base_info
        
        time.sleep(1)
    
    return stock_code_2_date_2_base_info

# 获取所有股票的枫红和融资次数
def stock_history_dividend():
    return ak.stock_history_dividend()

# 年度现金流表
# stock_code需要时带交易所前缀的，比如SH600519，SZ000651
def stock_cash_flow_sheet_by_yearly(stock_code):
    return ak.stock_cash_flow_sheet_by_yearly_em(stock_code)

# 股票编码转换，转成带交易所前缀的编码
def convert_stock_code(stock_code):
    # 上交所的编码前缀
    sh_prefix_list = [
        "6", 
        "9", 
        "688"
    ]

    # 如果是上交所的拼接sh
    for prefix in sh_prefix_list:
        if stock_code.startswith(prefix):
            return "SH" + stock_code

    # 深交所的编码前缀
    sz_prefix_list = [
        "000",
        "002",
        "300",
        "200"
    ]

    # 如果是深交所的，拼接sz
    for prefix in sz_prefix_list:
        if stock_code.startswith(prefix):
            return "SZ" + stock_code
    
    return stock_code

# 股票到日期到现金流信息
def stock_2_date_2_cash_flow_info(stock_codes):
    if len(stock_codes) == 0:
        return {}
    
    stock_2_date_2_info = {}
    for stock_code in stock_codes:
        # 转换成到交易所的编码
        code = convert_stock_code(stock_code)
        # 获取现金流表信息
        cash_flow_sheet = stock_cash_flow_sheet_by_yearly(code)
        cash_flow_sheet["LONG_ASSET_NETCASH_RATE"] = cash_flow_sheet["CONSTRUCT_LONG_ASSET"] / cash_flow_sheet["TOTAL_OPERATE_INFLOW"]

        stock_2_date_2_info[stock_code] = {}
        for cash_row in cash_flow_sheet.itertuples():
            date = datetime.strptime(cash_row.REPORT_DATE, "%Y-%m-%d %H:%M:%S").date()
            stock_2_date_2_info[stock_code][date] = {
                "LONG_ASSET_NETCASH_RATE": cash_row.LONG_ASSET_NETCASH_RATE
            }

    return stock_2_date_2_info