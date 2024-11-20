import cair_stock as cs
import constant.eastmoney_constant as const
import strategy.MeanReversionStrategyBaseResiduals as mr
import sys
from datetime import datetime
from model.account import account
from context.market_context import marketContext

class stockBackTesting:
    # 时间范围
    START_DATE = "20080101"
    END_DATE = datetime.now().strftime("%Y%m%d")

    # 开始偏移量
    START_OFFSET = 750
    # 单次交易股票数
    EXCHANGE_NUM = 1000
    # 两次交易时间间隔
    EXCHANGE_INTERVAL = 20
    # 初始现金
    INIT_CASH = 100000
    # 单次交易股票数
    EXCHANGE_NUM = 1000

    # 运行脚本
    def run(self, argv):
        # 获取输入参数
        if len(argv) != 2:
            exit(0)

        # 获取历史数据
        stock_history_dict = self.getStockHistory(argv, self.START_DATE, self.END_DATE)
        stock_daily_history_0 = stock_history_dict[argv[0]]
        stock_daily_history_1 = stock_history_dict[argv[1]]

        # 初始化账户
        user_account = account(self.INIT_CASH)
        print(user_account)

        # 获取股票共同交易的天数
        stock_length = stock_daily_history_0.shape[0]

        for i in range(self.START_OFFSET, stock_length):
            date = stock_daily_history_0.at[i, const.DATE]

            # 获取收盘见
            price_0 = stock_daily_history_0.at[i, const.CLOSE_PRICE_KEY]
            price_1 = stock_daily_history_1.at[i, const.CLOSE_PRICE_KEY]

            # 基于残差的均值回归策略判断
            result = mr.mean_reversion(stock_daily_history_0[const.CLOSE_PRICE_KEY].iloc[0:i], stock_daily_history_1[const.CLOSE_PRICE_KEY].iloc[0:i])
            if result != mr.BUY and result != mr.SELL:
                continue

            if result == mr.BUY:
                # 存在持仓股票，先卖出
                user_account.sell(argv[0], price_0, self.EXCHANGE_NUM)
                # 用现金买入
                buy_result = user_account.buy(argv[1], price_1, user_account.avilable_cash / price_1)
                if buy_result:
                    print("日期：", date)

            elif result == mr.SELL:
                # 存在持仓股票，先卖出
                user_account.sell(argv[1], price_1, self.EXCHANGE_NUM)
                # 用现金买入
                buy_result = user_account.buy(argv[0], price_0, user_account.avilable_cash / price_0)
                if buy_result:
                    print("日期：", date)

        print(user_account)
    
    # 获取输入的股票历史数据
    def getStockHistory(self, stock_codes, start_date, end_date):
        # 必须是2个代码
        if len(stock_codes) != 2:
            return {}

        # 股票A的每日历史信息
        stock_daily_history_0 = cs.stock_daily_history(stock_codes[0], start_date, end_date)
        stock_daily_history_1 = cs.stock_daily_history(stock_codes[1], start_date, end_date)

        # 计算有共同时间的历史数据
        stock_merge_list = cs.sync_data_list(stock_daily_history_0, stock_daily_history_1)

        return {
            stock_codes[0]: stock_merge_list[0],
            stock_codes[1]: stock_merge_list[1]
        }

# 执行脚本
argv = sys.argv[1:]
testing = stockBackTesting()
testing.run(argv)