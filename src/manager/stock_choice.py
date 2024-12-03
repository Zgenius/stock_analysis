import utils.stock_utils as cu
import utils.calculate_utils as su
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import math
from datetime import datetime, timedelta

"""
精选股票方法:
1.在中证A500的基金池中的股票
2.上时间超过10年的
3.过滤掉金融，房地产，医药，航空，汽车
4.ROE大于15%的
"""
def stock_choice(top = 20):
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
    # 每只股票的平均ROE
    stock_code_2_avg_ROE = {}
    for stock_code, date_2_ROE in stock_code_2_date_ROE.items():
        total_ROE = 0
        for ROE in date_2_ROE.values():
            # 过滤掉ROE，ROE是nan的在亏损
            if math.isnan(ROE):
                continue
            # ROE汇总
            total_ROE += ROE

        total_len = len(date_2_ROE)

        if total_len == 0:
            stock_code_2_avg_ROE[stock_code] = 0
        else:
            stock_code_2_avg_ROE[stock_code] = total_ROE / total_len

    # roe平均值降序排序
    stock_code_2_avg_ROE = su.dict_sort(stock_code_2_avg_ROE)

    # print(stock_code_2_date_ROE)
    for stock_code in stock_codes:
        if stock_code not in stock_code_2_date_ROE:
            continue
        # 获取股票时间范围内的所有ROE
        date_2_ROE = stock_code_2_date_ROE[stock_code]

        # 跳过ROE过低股票的标记
        jump_stock_code = False
        for ROE in date_2_ROE.values():
            # ROE存在小于15就跳过这只股票
            if math.isnan(ROE) or ROE < 15.0:
                jump_stock_code = True
                break

        # 满足ROE条件的记录下
        if not jump_stock_code:
            satisfied_ROE_stock_codes.append(stock_code)
    
    i = 0
    satisfied_stock_codes = []
    for stock_code in stock_code_2_avg_ROE:
        # 从roe最高的排序获取，获取top个,多余的就过滤掉
        if stock_code in satisfied_ROE_stock_codes and i < top:
            satisfied_stock_codes.append(stock_code)
            i += 1

    return satisfied_stock_codes