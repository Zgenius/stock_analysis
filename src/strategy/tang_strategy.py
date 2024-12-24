import manager.stock_choice as sc
import utils.date_utils as du
import utils.stock_utils as su
import utils.calculate_utils as cu
import constant.eastmoney_constant as const
import utils.util as util
import time
import math
from datetime import datetime, timedelta
from model.account import account
from model.grid_table import grid_table

'''
网红老唐策略
    三大前提
        1.利润为真
        2.利润可以持续
        3.维持当前利润，无需大量资本投入
'''
class tang_strategy:
    START_DATE = "20140101"
    END_DATE = datetime.now().strftime("%Y%m%d")

    # 初识金额
    TOTAL_CASH = 1000000


    SELL_POSITION = {
        50: 50,
        55: 80,
        60: 100
    }

    # 获取财务数据基础信息
    def annual_report(self):
        end_date = datetime.strptime(self.END_DATE, "%Y%m%d")
        # 去年
        last_year = end_date - timedelta(days = 365)
        # 十年前
        annual_report_dates = du.get_annual_report_dates(last_year, 16)

        # 获取财务数据基础信息
        return su.stock_2_date_base_info(annual_report_dates)
    
    # 过滤小不需要年份的年报，只保留输入日期内的
    def filter_annual_report(self, date_2_base_info, annual_report_dates):
        date_2_annual_report = {}
        for report_date in date_2_base_info.keys():
            if report_date not in annual_report_dates:
                continue
            date_2_annual_report[report_date] = date_2_base_info[report_date]

        return date_2_annual_report

    # 预估三年后净利润，以最近一年净利润为基础利润，以过去5年的净利润增长率为预估增长率
    def predict_net_profit_3_year(self, date_2_base_info):
        # 过去的净利润同比增长率
        net_profit_rate = []
        # 统计年份
        total_number = 0
        # 最近一年的净利润
        net_profit = 0
        net_proft_list = []
        for base_info in date_2_base_info.values():
            total_number += 1
            net_profit = base_info["净利润-净利润"]
            net_proft_list.append(base_info["净利润-净利润"])
            if not math.isnan(base_info["净利润-同比增长"]):
                net_profit_rate.append(base_info["净利润-同比增长"])
        
        if total_number == 0 or len(net_profit_rate) == 0:
            return 0
        
        # 过去的平均增长率，作为预估未来的增长率
        predict_growth_rate = sum(net_profit_rate) - max(net_profit_rate) / total_number / 100
        # 如果存在多个，取第二大的，如果只有一个，取这一个
        net_proft_list.sort(reverse = True)
        if len(net_proft_list) > 1:
            net_profit = net_proft_list[1]

        # 预计三年后净利润 当前利润 * 预计增长率的3次方
        return net_profit * (predict_growth_rate + 1) ** 3
    
    # 通过ROE计算持股最大仓位
    def compute_stock_position(self, stock_2_info):
        # 所有股票的总roe
        total_avg_ROE = 0
        for info in stock_2_info.values():
            total_avg_ROE += info['avg_ROE']

        stock_code_2_position = {}
        for stock_code, info in stock_2_info.items():
            stock_code_2_position[stock_code] = info["avg_ROE"] / total_avg_ROE
        
        return stock_code_2_position

    def run(self):
        # 选股
        # stock_codes = sc.stock_choice(10)
        choice_info = sc.stock_choice(10)
        stock_codes = choice_info["stock_codes"]
        stock_2_info = choice_info["stock_code_2_info"]
        # stock_codes = ['300628', '603288', '600519', '603605', '000651', '000333', '600887', '600690', '002475']
        print(stock_codes)

        # 股票数量
        stock_num = len(stock_codes)

        # 初始化账户
        user_account = account(self.TOTAL_CASH)
        print(user_account)

        # 初始化网格记录表
        table = grid_table()

        # 获取年报基础信息
        stock_code_2_date_2_base_info = self.annual_report()

        # 计算个股持股仓位上限
        stock_code_2_position = self.compute_stock_position(stock_2_info)

        # 记录股票编码到指标类信息的映射
        stock_code_2_indicator = {}
        # 股票编码到历史数据的映射表
        stock_code_2_history_info = {}
        # 股票除权除息信息
        stock_code_2_ex_rights = {}
        # 股票的一些基本信息
        stock_code_2_individual_info = {}
        for stock_code in stock_codes:
            # 历史数据
            stock_code_2_history_info[stock_code] = su.stock_daily_history(stock_code, self.START_DATE, self.END_DATE)
            # 获取pe等基础信息
            stock_code_2_indicator[stock_code] = su.stock_individual_indicator(stock_code)
            # 除权信息
            stock_code_2_ex_rights[stock_code] = su.stock_individual_ex_rights_detail(stock_code)
            # 股票的一些基本信息
            stock_code_2_individual_info[stock_code] = su.stock_individual_info(stock_code)

            time.sleep(1)

        # 时间范围内的所有天
        days = du.get_between_days(self.START_DATE, self.END_DATE)

        # 每天循环
        for day in days:
            date = day.date()
            # 去年
            last_year = date - timedelta(days = 365)
            # 五年前
            annual_report_dates = du.get_annual_report_dates(last_year, 5)

            for stock_code in stock_codes:
                # 不存在指标信息，就过滤
                if stock_code not in stock_code_2_indicator:
                    continue

                # 不存在历史信息就过滤
                if stock_code not in stock_code_2_history_info:
                    continue

                # 基本信息不存在
                if stock_code not in stock_code_2_individual_info:
                    continue

                # 过滤掉没有年报的股票
                if stock_code not in stock_code_2_date_2_base_info:
                    continue

                # 获取pe等基础信息
                stock_indicator = stock_code_2_indicator[stock_code]

                # 获取历史每天的信息
                stock_daily_history = stock_code_2_history_info[stock_code]

                # 基本信息
                stock_individual_info = stock_code_2_individual_info[stock_code]

                # 获取个股所有的除权除息信息
                ex_rights_resutl = cu.ex_rights(stock_code, user_account, table, stock_code_2_ex_rights, date)

                date_indicator = stock_indicator[stock_indicator["trade_date"] == date]
                if date_indicator.empty:
                    continue

                # 获取PE_TTM
                pe_ttm = date_indicator.get("pe_ttm").item()
                
                # 获取基础年报信息, 仅保留最近5年的，其他的删除
                date_2_base_info = self.filter_annual_report(stock_code_2_date_2_base_info[stock_code], annual_report_dates)
                # 预计的3年后的净利润
                predict_net_profit = self.predict_net_profit_3_year(date_2_base_info)
                # 3年后以20倍市盈率卖出的一半作为当前买入价格
                buy_market_value = predict_net_profit * 20 * 0.5
                # 总股本
                total_share_number = su.stock_individual_info_get(stock_individual_info, const.STOCK_INDIVIDUAL_TOTAL_SHARE_CAPITAL)
                
                # 合理买入价格
                reasonable_buy_sell = buy_market_value / total_share_number

                date_hitory = stock_daily_history[stock_daily_history[const.DATE] == date]
                if date_hitory.empty:
                    continue

                # 获取收盘价格
                close_price = date_hitory.get(const.CLOSE_PRICE_KEY).item()

                # 小于0的过滤掉
                if close_price <= 0:
                    continue

                # 获取当天账户总价值
                total_value = user_account.get_market_value_date(stock_code_2_history_info, date)

                # 单只股票持仓上限金额
                # single_limit_cash = total_value / stock_num
                single_limit_cash = total_value * stock_code_2_position[stock_code]
                # 股票持仓数量
                stock_holding_num = 0
                if stock_code in user_account.holding_stocks:
                    stock_holding_num = user_account.holding_stocks[stock_code].holding_num

                # 单只股票持仓价值
                stock_holding_value = stock_holding_num * close_price

                # 当前价格小于合理买入价格，就买入, 并且市盈率不能过高
                if close_price <= reasonable_buy_sell and pe_ttm <= 25:
                    # 股票当前应该持仓上限大于持仓上限10%的，就需要买入，也就是小与30%的就不管了
                    diff_rate = 1 - stock_holding_value / single_limit_cash
                    if diff_rate < 0.1:
                        continue

                    buy_cash = diff_rate * single_limit_cash

                    # 确定买入数量
                    number = util.can_buy_num(buy_cash, close_price)
                    buy_result = user_account.buy(stock_code, close_price, number)
                    if buy_result:
                        print("日期：", date, "pe_ttm: ", pe_ttm, "买入金额", number * close_price)
                        stock_holding_num += number
                
                if pe_ttm > 50:
                    diff_rate = stock_holding_value / single_limit_cash
                    if diff_rate < 0.5:
                        continue

                    # 计算买入金额 持仓比例 * 单只股票上限
                    sell_cash = diff_rate * (single_limit_cash * 0.5)

                    # 确定卖出数量
                    number = util.can_buy_num(sell_cash, close_price)
                    sell_result = user_account.sell(stock_code, close_price, number)
                    if sell_result:
                        print("日期：", date, "pe_ttm: ", pe_ttm, "卖出金额", number * close_price)
        
        print(user_account)
                
strategy = tang_strategy()
strategy.run()