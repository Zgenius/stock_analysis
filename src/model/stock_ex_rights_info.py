from sqlalchemy import Column, String, DateTime, BigInteger, Text, Float
from .base_model import BaseModel

class StockExRightsInfo(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), unique=True, index=True)
    name = Column(String(12))
    report_date = Column(DateTime)
    ex_rights_date = Column(DateTime)
    share_transfer_ratio = Column(Float)
    dividend_ratio = Column(Float)
    dividend_yield = Column(Float)
    extra_info = Column(Text)