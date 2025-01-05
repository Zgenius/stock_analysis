import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

'''
    画图管理器
    将画图的逻辑封装到这个类中
    减少重复代码
'''
class PlotManager:

    STYLE = 'seaborn-v0_8-darkgrid'

    def __init__(self):
        pass

    def show_line_chart(self, plot_dict):
        # 设置样式风格
        plt.style.use(self.STYLE)

        # 创建一个图表, 设置图片大小
        fig, ax = plt.subplots(figsize=(12, 6))

        # 设置图表标题并给坐标轴加上标签
        ax.set_title(plot_dict['title'], fontsize=20, fontweight="bold", color="#333333")
        ax.set_xlabel(plot_dict['xlabel'], fontsize=14)
        ax.set_ylabel(plot_dict['ylabel'], fontsize=14)

        x_values = plot_dict['x_values']

        # 设置刻度标记的大小
        ax.tick_params(axis='both', which = 'major', labelsize=10)
        # 获取所有Y的数据
        y_values_list = plot_dict['y_values_list']
        for y_values_record in y_values_list:
            y_values = y_values_record['values']
            # 折线图
            ax.plot(x_values, y_values, 'o-', label = y_values_record['label'], linewidth=2, markersize=8)
            # 当鼠标放上去的时候，每个x值的点的y值显示出来
            for i in range(len(x_values)):
                ax.annotate(f"{y_values[i]:.2f}", (x_values[i], y_values[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)

        # 禁止 y 轴使用科学计数法
        # formatter = ScalarFormatter(useOffset=False)
        # formatter.set_scientific(False)
        # ax.yaxis.set_major_formatter(formatter)

        # 调整坐标轴
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 添加图例
        ax.legend(fontsize=12, loc="upper left")

        # 设置中文字体为黑体（SimHei），你可以根据系统字体情况替换为其他中文字体
        # plt.rcParams['font.sans-serif'] = ['SimSong']  
        plt.rcParams['font.sans-serif'] = ['Kai']  
        # 解决负号显示问题
        plt.rcParams['axes.unicode_minus'] = False  

        # 调整布局
        plt.tight_layout()

        plt.show()