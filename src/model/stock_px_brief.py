from sqlalchemy import Column, String, DateTime, BigInteger, Text, Float
from .base_model import BaseModel

class StockPxBrief(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), index=True)
    name = Column(String(12))
    trade_date = Column(DateTime)  # 交易日
    pe = Column(Float)  # 市盈率
    pe_ttm = Column(Float)  # 市盈率TTM
    pb = Column(Float)  # 市净率
    ps = Column(Float)  # 市销率
    ps_ttm = Column(Float)  # 市销率TTM
    dv_ratio = Column(Float)  # 股息率
    dv_ttm = Column(Float)  # 股息率TTM
    pcf = Column(Float)  # 实现率
    peg = Column(Float)  # peg
    negotiable_shares = Column(Float)  # 流通股本
    total_mv = Column(Float)  # 总市值
    extra_info = Column(Text)