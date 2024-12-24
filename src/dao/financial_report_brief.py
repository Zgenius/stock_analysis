from dao.BaseModel import BaseModel
from peewee import CharField, DateTimeField, BigIntegerField, TextField, DoubleField

class financial_report_brief(BaseModel):
    id = BigIntegerField()
    symbol = CharField(max_length=12)
    name = CharField(max_length=12)
    report_time = DateTimeField()
    operating_revenue = DoubleField()
    net_profit = DoubleField()
    net_asset_value_per_share = DoubleField()
    earnings_per_share = DoubleField()
    operating_cash_flow_per_share = DoubleField()
    return_on_equity = DoubleField()
    gross_profit_ratio = DoubleField()
    extra_info = TextField()