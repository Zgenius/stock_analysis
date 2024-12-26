from dao.BaseModel import BaseModel
from peewee import CharField, DateTimeField, BigIntegerField, TextField, DoubleField

class StockExRightsInfo(BaseModel):
    id = BigIntegerField
    symbol = CharField(max_length=12)
    name = CharField(max_length=12)
    report_date = DateTimeField()
    ex_rights_date = DateTimeField()
    share_transfer_ratio = DoubleField()
    dividend_ratio = DoubleField()
    dividend_yield = DoubleField()
    extra_info = TextField()