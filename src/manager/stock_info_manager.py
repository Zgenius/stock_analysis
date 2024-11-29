import utils.stock_utils as su

def stock_ROE(stock_codes, date_list):
    # 循环查询每个日期的净资产收益率
    stock_code_2_date_ROE = {}
    for date in date_list:
        # 获取存在roe的基础信息
        stock_code_2_base_info = su.stock_code_2_base_info(date)
        # 只保留输入股票编码的基础信息，其他的过滤掉
        for stock_code in stock_codes:
            # 不存在信息，就过滤掉
            if stock_code not in stock_code_2_base_info:
                continue

            # 初始化下字典key
            if stock_code not in stock_code_2_date_ROE:
                stock_code_2_date_ROE[stock_code] = {}

            # 获取个股的roe等基本信息
            stock_base_info = stock_code_2_base_info.get(stock_code)
            stock_code_2_date_ROE[stock_code][date] = stock_base_info["净资产收益率"]
    
    return stock_code_2_date_ROE