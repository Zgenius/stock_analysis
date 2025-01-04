import matplotlib.pyplot as plt
import matplotlib
from sqlalchemy import and_
from model.financial_report_brief import FinancialReportBrief
from matplotlib.ticker import ScalarFormatter
from datetime import datetime, timedelta

class netProftStatistics:
    def __init__(self):
        pass

    def show(self, symbol):
        end_date = datetime.now()
        start_date = end_date - timedelta(days = 365 * 15)
        # print(matplotlib.get_configdir())
        where = and_(FinancialReportBrief.symbol == symbol, FinancialReportBrief.report_time.like("%12-31%"), FinancialReportBrief.report_time >= start_date)
        briefs = FinancialReportBrief.select(FinancialReportBrief.report_time, FinancialReportBrief.net_profit, FinancialReportBrief.operating_revenue).where(where).order_by(FinancialReportBrief.report_time).all()
        # 获取briefs里所有的净利润
        net_profits = [round(brief.net_profit / 100000000, 2) for brief in briefs]
        # 获取briefs里所有的报告时间
        report_times = [brief.report_time.strftime("%Y") for brief in briefs]
        # 获取briefs里所有的营业收入
        operating_revenues = [round(brief.operating_revenue / 100000000, 2) for brief in briefs]

        fig, ax = plt.subplots()

        # linewidth: 线宽
        ax.plot(net_profits, linewidth=3)

        # 在增加一条线
        ax.plot(operating_revenues, linewidth=3)

        # 设置X轴的刻度值
        ax.set_xticklabels(report_times, rotation=45, fontsize=1)

        # 设置图表标题并给坐标轴加上标签
        ax.set_title("净利润走势", fontsize=24)
        ax.set_xlabel("年份", fontsize=10)
        ax.set_ylabel("净利润(亿)", fontsize=10)
        # 设置坐标轴轴标题显示中文

        # 设置刻度标记的大小
        ax.tick_params(axis='both', labelsize=10)

        # 禁止 y 轴使用科学计数法
        formatter = ScalarFormatter(useOffset=False)
        formatter.set_scientific(False)
        ax.yaxis.set_major_formatter(formatter)
        
        # linewidth: 线宽
        ax.scatter(report_times, net_profits, s=20)
        ax.scatter(report_times, operating_revenues, s=20)

        # 当鼠标放上去的时候，每个x值的点的y值显示出来
        for i in range(len(report_times)):
            plt.text(i, net_profits[i], net_profits[i], ha='center', va='bottom', fontsize=10)
            plt.text(i, operating_revenues[i], operating_revenues[i], ha='center', va='bottom', fontsize=10)

        plt.style.use('seaborn-v0_8')

        # # 设置下方的间距
        # plt.subplots_adjust(bottom=0.2)
        # # 调整左边边框的宽度
        # plt.subplots_adjust(left=0.2)

        # 设置中文字体为黑体（SimHei），你可以根据系统字体情况替换为其他中文字体
        plt.rcParams['font.sans-serif'] = ['SimSong']  
        # 解决负号显示问题
        plt.rcParams['axes.unicode_minus'] = False  
        # 设置图片大小
        fig.set_size_inches(12, 6)

        plt.show()

if __name__ == "__main__":
    np = netProftStatistics()
    np.show("300628")