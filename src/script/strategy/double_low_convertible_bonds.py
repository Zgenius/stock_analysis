'''
双低可转债策略量化
买入策略
    1.低可转债价格
    2.低溢价率
卖出策略
    1.可转债到强赎价格
    2.溢价率超过30%并且距离买入价格涨幅超过30%
'''

import akshare as ak
import pandas as pd
import numpy as np
import datetime
import time

# 获取可转债列表
def get_cb_bond_list():
    df = ak.bond_zh_cov()
    return df['债券代码'].tolist()

# 获取可转债实时数据
def get_cb_bond_realtime():
    df = ak.bond_zh_hs_cov_spot()

    # 打印字段名称和数据，用于调试
    print("字段名称:", df.columns)
    print("数据示例:\n", df.head())
    return df

# 双低可转债策略
def double_low_cb_strategy(bond_list, start_date, end_date):
    portfolio = {}  # 持仓
    portfolio_returns = []  # 每日收益率
    
    for date in pd.date_range(start_date, end_date):
        time.sleep(0.1)
        date_str = date.strftime('%Y%m%d')
        
        # 获取实时数据
        df = get_cb_bond_realtime()
        if df.empty:
            continue
        
        # 筛选符合条件的可转债
        for bond_code in bond_list:
            bond_data = df[df['code'] == bond_code]
            if bond_data.empty:
                continue
            
            # 获取价格和溢价率，并转换为数值类型
            try:
                price = float(bond_data.iloc[0]['trade'])  # 最新价
                premium_rate = float(bond_data.iloc[0]['changepercent'])  # 涨跌幅（假设为溢价率）
            except (ValueError, KeyError) as e:
                print(f"可转债 {bond_code} 的数据格式错误: {e}")
                continue
            
            # 买入条件
            if (price < 120) and (premium_rate < 20) and (bond_code not in portfolio):
                portfolio[bond_code] = {'buy_price': price, 'buy_date': date}
        
        # 卖出逻辑
        for bond_code in list(portfolio.keys()):
            bond_data = df[df['code'] == bond_code]
            if bond_data.empty:
                continue
            
            # 获取当前价格和溢价率，并转换为数值类型
            try:
                current_price = float(bond_data.iloc[0]['trade'])
                current_premium_rate = float(bond_data.iloc[0]['changepercent'])
            except (ValueError, KeyError) as e:
                print(f"可转债 {bond_code} 的数据格式错误: {e}")
                continue
            
            buy_price = portfolio[bond_code]['buy_price']
            
            # 卖出条件 1：达到强赎价格
            if current_price >= 130:
                del portfolio[bond_code]
            
            # 卖出条件 2：溢价率超过 30% 且涨幅超过 30%
            if (current_premium_rate > 30) and (current_price / buy_price > 1.3):
                del portfolio[bond_code]
        
        # 计算当日收益率
        daily_return = 0
        for bond_code in portfolio:
            bond_data = df[df['code'] == bond_code]
            if bond_data.empty:
                continue
            try:
                current_price = float(bond_data.iloc[0]['trade'])
                buy_price = portfolio[bond_code]['buy_price']
                if buy_price == 0:
                    print(f"可转债 {bond_code} 的买入价格为 0，跳过计算")
                    continue
                daily_return += (current_price - buy_price) / buy_price * 0.05  # 单只可转债仓位5%
            except (ValueError, KeyError) as e:
                print(f"可转债 {bond_code} 的数据格式错误: {e}")
                continue
        portfolio_returns.append(daily_return)
    
    # 计算累计收益率
    cumulative_returns = (1 + pd.Series(portfolio_returns)).cumprod()
    
    return cumulative_returns

# 主程序
if __name__ == "__main__":
    # 参数设置
    bond_list = get_cb_bond_list()
    start_date = '20200101'
    end_date = '20231231'
    
    # 运行策略
    cumulative_returns = double_low_cb_strategy(bond_list, start_date, end_date)
    
    # 输出结果
    print("累计收益率:\n", cumulative_returns)
    
    # 绘制收益率曲线
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns, label='双低可转债策略')
    plt.title('双低可转债策略累计收益率')
    plt.xlabel('时间')
    plt.ylabel('收益率')
    plt.legend()
    plt.show()