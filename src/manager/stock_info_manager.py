import utils.stock_utils as su

# 获取股票的基础信息
def stock_2_date_indicator(stock_codes, date_list, stock_code_2_date_2_base_info, indicator):
    # 循环查询每个日期的净资产收益率
    stock_code_2_date_indicator = {}
    for date in date_list:
        # 只保留输入股票编码的基础信息，其他的过滤掉
        for stock_code in stock_codes:
            # 不存在信息，就过滤掉
            if stock_code not in stock_code_2_date_2_base_info:
                continue

            date_2_base_info = stock_code_2_date_2_base_info[stock_code]
            if date not in date_2_base_info:
                continue

            # 初始化下字典key
            if stock_code not in stock_code_2_date_indicator:
                stock_code_2_date_indicator[stock_code] = {}

            # 获取个股的roe等基本信息
            stock_base_info = date_2_base_info[date]
            stock_code_2_date_indicator[stock_code][date] = stock_base_info[indicator]
    
    return stock_code_2_date_indicator

# 计算股票的净现比
def stock_code_date_2_OCF(stock_code_2_date_2_base_info):
    stock_code_2_date_2_OCF = {}
    for stock_code, date_2_base_info in stock_code_2_date_2_base_info.items():
        # 初始化下
        if stock_code not in stock_code_2_date_2_OCF:
            stock_code_2_date_2_OCF[stock_code] = {}
        
        date_2_OCF = stock_code_2_date_2_OCF[stock_code]
        
        for date, base_info in date_2_base_info.items():
            # 每股净利润
            earnings_per_share = base_info["每股收益"]
            if earnings_per_share == 0:
                date_2_OCF[date] = 0
                continue

            # 美股现金流
            cash_flow_per_share = base_info["每股经营现金流量"]
            # 净现比
            date_2_OCF[date] = cash_flow_per_share / earnings_per_share

        stock_code_2_date_2_OCF[stock_code] = date_2_OCF
    
    return stock_code_2_date_2_OCF