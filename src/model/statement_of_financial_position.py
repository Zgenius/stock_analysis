from sqlalchemy import Column, String, DateTime, BigInteger, Text, Float
from .base_model import BaseModel

# 资产负债表
class StatementOfFinancialPosition(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(12), index=True)
    name = Column(String(12))
    report_date = Column(DateTime)
    extra_info = Column(Text) # 资产负债表详细信息都放在这里吧