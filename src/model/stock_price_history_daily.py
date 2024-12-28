from sqlalchemy import Column, String, DateTime, BigInteger, Text, Float
from .base_model import BaseModel

class StockPriceHistoryDaily(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), index=True)
    name = Column(String(12))
    trade_date = Column(DateTime)  # 交易日
    opening_price = Column(Float)
    closing_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)
    amplitude = Column(Float)
    percentage_change = Column(Float)
    price_change = Column(Float)
    turnover_rate = Column(Float)
    extra_info = Column(Text)