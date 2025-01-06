from sqlalchemy import and_
from model.financial_report_brief import FinancialReportBrief
from datetime import datetime, timedelta
from manager.plot_manager import PlotManager
from model.stock_basic_info import StockBasicInfo

#最近15年的营业收入和净利润
class netProftStatistics:
    def __init__(self):
        pass

    def show(self, symbol):
        end_date = datetime.now()
        start_date = end_date - timedelta(days = 365 * 15)

        stock = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).where(StockBasicInfo.symbol == symbol).distinct().order_by(StockBasicInfo.symbol.asc()).one()
        # print(matplotlib.get_configdir())
        where = and_(FinancialReportBrief.symbol == symbol, FinancialReportBrief.report_time.like("%12-31%"), FinancialReportBrief.report_time >= start_date)
        briefs = FinancialReportBrief.select(FinancialReportBrief.report_time, FinancialReportBrief.net_profit, FinancialReportBrief.operating_revenue).where(where).order_by(FinancialReportBrief.report_time).all()
        # 获取briefs里所有的净利润
        net_profits = [round(brief.net_profit / 100000000, 2) for brief in briefs]
        # 获取briefs里所有的报告时间
        report_times = [brief.report_time.strftime("%Y") for brief in briefs]
        # 获取briefs里所有的营业收入
        operating_revenues = [round(brief.operating_revenue / 100000000, 2) for brief in briefs]

        plot_dict = {
            'title': stock.name + '-净利润走势',
            'xlabel': '年份',
            'ylabel': '净利润(亿)',
            'x_values': report_times,
            'y_values_list': [
                {
                    'label': '营业收入',
                    'values': operating_revenues,
                },
                {
                    'label': '净利润',
                    'values': net_profits,
                }
            ]
        }

        plot_mnaager = PlotManager()
        plot_mnaager.show_line_chart(plot_dict)

if __name__ == "__main__":
    np = netProftStatistics()
    np.show("600519")