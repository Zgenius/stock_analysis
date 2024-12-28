from sqlalchemy import Column, String, DateTime, BigInteger, Text, Float
from .base_model import BaseModel

class FinancialReportBrief(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), index=True)
    name = Column(String(12))
    report_time = Column(DateTime)
    operating_revenue = Column(Float)
    net_profit = Column(Float)
    net_asset_value_per_share = Column(Float)
    earnings_per_share = Column(Float)
    operating_cash_flow_per_share = Column(Float)
    return_on_equity = Column(Float)
    gross_profit_ratio = Column(Float)
    extra_info = Column(Text)