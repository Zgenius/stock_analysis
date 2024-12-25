from dao.BaseModel import BaseModel
from peewee import CharField, DateTimeField, BigIntegerField, TextField, DoubleField

class stock_price_history_daily(BaseModel):
    id = BigIntegerField()
    symbol = CharField(max_length=12)
    name = CharField(max_length=12)
    # 交易日
    trade_date = DateTimeField()
    opening_price = DoubleField()
    closing_price = DoubleField()
    high_price = DoubleField()
    low_price = DoubleField()
    volume = DoubleField()
    turnover = DoubleField()
    amplitude = DoubleField()
    percentage_change = DoubleField()
    price_change = DoubleField()
    turnover_rate = DoubleField()
    extra_info = TextField()