# from manager.plot_manager import PlotManager

# plot_dict = {
#     'title': '市场份额',
#     'labels': ["产品A", "产品B", "产品C", "产品D"],
#     'sizes': [40, 30, 20, 10],  # 各部分的大小
#     'explode': (0.1, 0, 0, 0),  # 突出显示某一部分
#     'xlabel': '产品类别',
#     'ylabel': '市场份额 (%)',
# }

# plot_mnaager = PlotManager()
# plot_mnaager.show_pie_chart(plot_dict)

import akshare as ak

stock_zh_index_value_csindex_df = ak.stock_zh_index_value_csindex(symbol="H30374")
print(stock_zh_index_value_csindex_df)

