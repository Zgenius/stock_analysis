import utils.stock_utils as cu
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
from datetime import datetime, timedelta

"""
精选股票方法:
1.在中证A500的基金池中的股票
2.上时间超过10年的
3.过滤掉金融，房地产，医药，航空，汽车
4.ROE大于15%的
"""
def stock_choice():
    now = datetime.now()
    earliest_availability = now - timedelta(days = 365 * 5)

    annual_report_dates = [
        "20101231",
        "20111231",
        "20121231",
        "20131231",
        "20141231",
        "20151231",
        "20161231",
        "20171231",
        "20181231",
        "20191231",
        "20201231",
        "20211231",
        "20221231",
        "20231231",
    ]

    # 需要过滤掉的行业
    filter_sector_names = [
        "证券",
        "保险",
        "房地产开发",
        "房地产服务",
        "中药",
        "医疗服务",
        "医疗器械",
        "贸易行业",
        "纺织服装",
        "农牧饲渔",
        "物流行业",
        "航空机场",
        "商业百货"
    ]

    stock_codes = []
    # 所有股票信息
    stocks = cu.index_contain_stocks(fc.CODE_ZZ_A500)
    for index, row in stocks.iterrows():
        stock_info = cu.stock_individual_info(row[const.FUND_CONTAINS_STOCK_CODE])
        stock_availability = datetime.strptime(str(cu.stock_individual_info_get(stock_info, const.STOCK_AVAILABILITY)), "%Y%m%d")
        # 如果上市时间不小于可接受的最早上市时间，就过滤掉
        if stock_availability > earliest_availability:
            continue

        # 过滤掉行业：医疗，地产，金融，汽车
        sector_name = cu.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_SECTOR)
        if sector_name in filter_sector_names:
            continue

        # 记录下满足条件的编码
        stock_codes.append(cu.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_CODE))
    # print(stock_codes)

    satisfied_ROE_stock_codes = []
    # 获取股票每年的ROE
    stock_code_2_date_ROE = sim.stock_ROE(stock_codes, annual_report_dates)
    # print(stock_code_2_date_ROE)
    for index, stock_code in enumerate(stock_codes):
        if stock_code not in stock_code_2_date_ROE:
            continue
        # 获取股票时间范围内的所有ROE
        date_2_ROE = stock_code_2_date_ROE[stock_code]

        # 跳过ROE过低股票的标记
        jump_stock_code = False
        for ROE in date_2_ROE.values():
            # ROE存在小于15就跳过这只股票
            if ROE < 15.0:
                jump_stock_code = True
                break

        # 满足ROE条件的记录下
        if not jump_stock_code:
            satisfied_ROE_stock_codes.append(stock_code)

    return satisfied_ROE_stock_codes