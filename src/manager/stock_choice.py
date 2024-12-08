import utils.stock_utils as cu
import utils.calculate_utils as su
import constant.eastmoney_constant as const
import constant.fund_code_constant as fc
import manager.stock_info_manager as sim
import utils.date_utils as du
import math
from datetime import datetime, timedelta

# 获取年报日期
def get_annual_report_dates(end_date):
    # 十年前
    ten_year_ago = end_date - timedelta(days = 365 * 10)
    # 获取所有年份
    year_dates = du.get_between_years(ten_year_ago, end_date)
    
    annual_report_dates = []
    for year_date in year_dates:
        annual_report_dates.append(datetime(year_date.year, 12, 31).strftime("%Y%m%d"))
    
    return annual_report_dates

# 获取最新财报日期
def get_newest_report_date(end_date):
    report_dates = [
        datetime(end_date.year, 9, 30),
        datetime(end_date.year, 7, 30),
        datetime(end_date.year, 3, 31)
    ]

    for report_date in report_dates:
        if end_date > report_date:
            return report_date
    
    return None

"""
精选股票方法:
1.在中证A500的基金池中的股票
2.上时间超过10年的
3.过滤掉金融，房地产，医药，航空，汽车
4.平均ROE大于15%的
5.存在一年ROE小于12%的不要

选出股票之后，需要查看年报和行业同等地位公司年报，观察公司
1.盈利是否真实
2.保持现有盈利是否需要大量资本投入
3.盈利是否可持续
"""
def stock_choice(top = 20):
    now = datetime.now()
    # 去年
    last_year = now - timedelta(days = 365)
    # 十年前
    annual_report_dates = get_annual_report_dates(last_year)

    newest_report_date = get_newest_report_date(now)

    # 5年前
    earliest_availability = now - timedelta(days = 365 * 5)

    # 需要过滤掉的行业
    filter_sector_names = [
        "证券",
        "保险",
        # "银行",
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
        "商业百货",
        "环保行业",
        "化学制药"
    ]

    # 获取股票分红和融资次数等信息
    # stock_history_dividend = cu.stock_history_dividend()

    stock_code_list = []
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
        stock_code_list.append(cu.stock_individual_info_get(stock_info, const.STOCK_INDIVIDUAL_CODE))

    # 获取财务数据基础信息
    stock_code_2_date_2_base_info = cu.stock_2_date_base_info(annual_report_dates)

    stock_codes = []
    # 获取最新年报基本信息
    stock_code_2_newest_base_info = {}
    if newest_report_date != None:
        newest_report_date = newest_report_date.strftime("%Y%m%d")
        stock_code_2_newest_base_info = cu.stock_code_2_base_info(newest_report_date)
    
    # 判断最新财报的营业收入负增长了-20%，就过滤掉
    for stock_code in stock_code_list:
        if stock_code in stock_code_2_newest_base_info:
            newest_base_info = stock_code_2_newest_base_info[stock_code]
            # 判断最新财报的营业收入负增长了-20%，就过滤掉
            if newest_base_info["营业收入-同比增长"] < -10:
                continue

            # 判断最新财报的净利润负增长了-20%，就过滤掉
            if newest_base_info["净利润-同比增长"] < 0:
                continue
        
        stock_codes.append(stock_code)

    # 获取股票每年的ROE
    stock_code_2_date_ROE = sim.stock_2_date_indicator(stock_codes, annual_report_dates, stock_code_2_date_2_base_info, "净资产收益率")
    # 每只股票的平均ROE
    stock_code_2_avg_ROE = su.stock_code_2_avg(stock_code_2_date_ROE)
    # roe平均值降序排序
    stock_code_2_avg_ROE = su.dict_sort(stock_code_2_avg_ROE)

    # 满足ROE的股票编码
    satisfied_ROE_stock_codes = []
    # 过滤掉这些年中，存在一年roe小于8%的股票
    for stock_code in stock_codes:
        if stock_code not in stock_code_2_date_ROE:
            continue
        # 获取股票时间范围内的所有ROE
        date_2_ROE = stock_code_2_date_ROE[stock_code]

        # 跳过ROE过低股票的标记
        jump_stock_code = False
        for ROE in date_2_ROE.values():
            # ROE存在小于8%就跳过这只股票
            if math.isnan(ROE) or ROE < 12:
                jump_stock_code = True
                break

        # 满足ROE条件的记录下
        if not jump_stock_code:
            satisfied_ROE_stock_codes.append(stock_code)
    
    # 获取股票每年的净利润同比增长率
    stock_code_2_date_YOY_net_profit_growth = sim.stock_2_date_indicator(stock_codes, annual_report_dates, stock_code_2_date_2_base_info, "净利润-同比增长")
    # 每只股票的平均净利润环比增长率
    stock_code_2_avg_YOY_net_profit_growth = su.stock_code_2_avg(stock_code_2_date_YOY_net_profit_growth)
    # 净利润环比增长率降序排序
    stock_code_2_avg_YOY_net_profit_growth = su.dict_sort(stock_code_2_avg_YOY_net_profit_growth)
    
    # 过滤掉异常的净利润同比增长率的股票
    satisfied_net_profit_stock_codes = []
    for stock_code in stock_codes:
        if stock_code not in stock_code_2_date_YOY_net_profit_growth:
            continue

        date_2_YOY_net_profit_growth = stock_code_2_date_YOY_net_profit_growth[stock_code]

        jump_stock_code = False
        for YOY_net_profit_growth in date_2_YOY_net_profit_growth.values():
            if math.isnan(YOY_net_profit_growth):
                continue

            # 存在某年净利润同比增长率下跌超过20%的不要，净利润增长大于100%一般都是去年基数过低的，不要
            if YOY_net_profit_growth > 150 or YOY_net_profit_growth < -20:
                jump_stock_code = True

        if not jump_stock_code:
            satisfied_net_profit_stock_codes.append(stock_code)

    # 计算净现比
    stock_code_2_date_OCF = sim.stock_code_date_2_OCF(stock_code_2_date_2_base_info)
    stock_code_2_avg_OCF = su.stock_code_2_avg(stock_code_2_date_OCF)
    # 净现比合格的股编码
    satisfied_OCF_stock_codes = []
    for stock_code in stock_codes:
        if stock_code not in stock_code_2_date_OCF:
            continue

        date_2_OCF = stock_code_2_date_OCF[stock_code]
        jump_stock_code = False
        for avg_OCF in date_2_OCF.values():
            if math.isnan(avg_OCF):
                continue

            # 净现比至少0
            if avg_OCF <= 0:
                jump_stock_code = True

        if not jump_stock_code:
            satisfied_OCF_stock_codes.append(stock_code)

    i = 0
    satisfied_stock_codes = []
    for stock_code, avg_ROE in stock_code_2_avg_ROE.items():
        # 获取分红融资次数信息
        # stock_dividend = stock_history_dividend[stock_history_dividend["代码"] == stock_code]
        # 过滤掉融资次数过多的股票
        # if len(stock_dividend) > 0:
        #     if stock_dividend.get("融资次数").item() > 0:
        #         continue

        avg_OCF = stock_code_2_avg_OCF[stock_code]
        # 平均净现比小于1的过滤掉
        if avg_OCF < 1:
            continue

        # 平均ROE小于20不要
        if avg_ROE < 20:
            continue

        # 不满足净利润要求不满足的过滤掉
        if stock_code not in satisfied_net_profit_stock_codes:
            continue

        # 不满足净现比的也过滤掉
        if stock_code not in satisfied_OCF_stock_codes:
            continue

        # 存在任何一年roe过低的过滤掉
        if stock_code not in satisfied_ROE_stock_codes:
            continue

        # 从roe最高的排序获取，获取top个,多余的就过滤掉,并且满足净利润没有负增长的股票
        if i < top:
            satisfied_stock_codes.append(stock_code)
            i += 1

    return satisfied_stock_codes