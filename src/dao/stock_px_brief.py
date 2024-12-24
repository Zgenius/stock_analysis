from dao.BaseModel import BaseModel
from peewee import CharField, DateTimeField, BigIntegerField, TextField, DoubleField

class stock_px_brief(BaseModel):
    id = BigIntegerField()
    symbol = CharField(max_length=12)
    name = CharField(max_length=12)
    # 交易日
    trade_date = DateTimeField()
    # 市盈率
    pe = DoubleField()
    # 市盈率TTM
    pe_ttm = DoubleField()
    # 市净率
    pb = DoubleField()
    # 市销率
    ps = DoubleField()
    # 市销率TTM
    ps_ttm = DoubleField()
    # 股息率
    dv_ratio = DoubleField()
    # 股息率TTM
    dv_ttm = DoubleField()
    # 总市值
    total_mv = DoubleField()
    extra_info = TextField()