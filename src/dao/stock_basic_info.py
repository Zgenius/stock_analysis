from dao.BaseModel import BaseModel
from peewee import CharField, DateTimeField, BigIntegerField, TextField

class stock_basic_info(BaseModel):
    id = CharField
    symbol = CharField(max_length=12)
    name = CharField(max_length=12)
    sector = CharField(max_length=128)
    listing_time = DateTimeField()
    total_share_capital = BigIntegerField()
    extra_info = TextField()
    # create_time = DateTimeField()
    # update_time = DateTimeField(null = True)