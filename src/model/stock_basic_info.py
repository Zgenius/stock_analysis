from sqlalchemy import Column, String, DateTime, BigInteger, Text
from .base_model import BaseModel

class StockBasicInfo(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), unique=True, index=True)
    name = Column(String(12))
    sector = Column(String(128))
    listing_time = Column(DateTime)
    total_share_capital = Column(BigInteger)
    extra_info = Column(Text)