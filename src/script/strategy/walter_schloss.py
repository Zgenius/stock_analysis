import akshare as ak
import pandas as pd
import numpy as np
import datetime

# 获取股票列表
def get_stock_list():
    df = ak.stock_info_a_code_name()
    return df['code'].tolist()

# 获取股票历史数据
def get_stock_data(stock_code, start_date, end_date):
    df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    return df

# 获取财务数据（负债率）
def get_financial_data(stock_code):
    try:
        # 获取资产负债表
        df = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
        if not df.empty:
            # 检查返回的数据结构
            print(f"股票 {stock_code} 的财务数据列名: {df.columns}")
            # 假设负债合计和资产总计的列名分别为 '负债合计' 和 '资产总计'
            if '负债合计' in df.columns and '资产总计' in df.columns:
                total_liab = df[df['项目'] == '负债合计'].iloc[0]['最新值']
                total_assets = df[df['项目'] == '资产总计'].iloc[0]['最新值']
                debt_ratio = total_liab / total_assets
                return debt_ratio
            else:
                print(f"股票 {stock_code} 的财务数据缺少必要列")
        else:
            print(f"股票 {stock_code} 的财务数据为空")
    except Exception as e:
        print(f"获取股票 {stock_code} 的财务数据失败: {e}")
    return None

# 筛选烟蒂股
def filter_cigar_butt_stocks(stock_list, date):
    cigar_butt_stocks = []
    
    for stock_code in stock_list:
        # 获取历史数据
        start_date = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.timedelta(days=3*365)).strftime('%Y%m%d')
        df = get_stock_data(stock_code, start_date, date)
        
        if df.empty:
            continue
        
        # 计算最低价
        min_price = df['最低'].min()
        current_price = df.iloc[-1]['收盘']
        
        # 获取财务数据
        debt_ratio = get_financial_data(stock_code)
        if debt_ratio is None:
            continue
        
        # 获取PE和PB
        stock_pe_pb = ak.stock_a_lg_indicator(stock_code)
        if stock_pe_pb.empty:
            continue
        pe = stock_pe_pb.iloc[0]['市盈率']
        pb = stock_pe_pb.iloc[0]['市净率']
        
        # 筛选条件
        if (pe < 15) and (pb < 0.67) and (current_price <= min_price * 1.2) and (debt_ratio < 0.5):
            cigar_butt_stocks.append(stock_code)
    
    return cigar_butt_stocks

# 烟蒂股策略
def cigar_butt_strategy(stock_list, start_date, end_date):
    portfolio = {}  # 持仓
    portfolio_returns = []  # 每日收益率
    
    for date in pd.date_range(start_date, end_date):
        date_str = date.strftime('%Y%m%d')
        
        # 筛选烟蒂股
        cigar_butt_stocks = filter_cigar_butt_stocks(stock_list, date_str)
        
        # 买入新股票
        for stock_code in cigar_butt_stocks:
            if stock_code not in portfolio:
                df = get_stock_data(stock_code, date_str, date_str)
                if not df.empty:
                    portfolio[stock_code] = {'buy_price': df.iloc[0]['收盘'], 'buy_date': date}
        
        # 卖出逻辑
        for stock_code in list(portfolio.keys()):
            df = get_stock_data(stock_code, date_str, date_str)
            if df.empty:
                continue
            current_price = df.iloc[0]['收盘']
            buy_price = portfolio[stock_code]['buy_price']
            buy_date = portfolio[stock_code]['buy_date']
            
            # 涨幅超过50%，卖出50%
            if current_price / buy_price > 1.5:
                del portfolio[stock_code]
            
            # 持仓超过1年且不符合条件，卖出
            if (date - buy_date).days > 365 and stock_code not in cigar_butt_stocks:
                del portfolio[stock_code]
        
        # 计算当日收益率
        daily_return = 0
        for stock_code in portfolio:
            df = get_stock_data(stock_code, date_str, date_str)
            if df.empty:
                continue
            current_price = df.iloc[0]['收盘']
            buy_price = portfolio[stock_code]['buy_price']
            daily_return += (current_price - buy_price) / buy_price * 0.05  # 单只股票仓位5%
        portfolio_returns.append(daily_return)
    
    # 计算累计收益率
    cumulative_returns = (1 + pd.Series(portfolio_returns)).cumprod()
    
    return cumulative_returns

# 主程序
if __name__ == "__main__":
    # 参数设置
    stock_list = get_stock_list()
    start_date = '20200101'
    end_date = '20231231'
    
    # 运行策略
    cumulative_returns = cigar_butt_strategy(stock_list, start_date, end_date)
    
    # 输出结果
    print("累计收益率:\n", cumulative_returns)
    
    # 绘制收益率曲线
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns, label='烟蒂股策略')
    plt.title('烟蒂股策略累计收益率')
    plt.xlabel('时间')
    plt.ylabel('收益率')
    plt.legend()
    plt.show()