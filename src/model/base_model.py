from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import insert
from utils import util
from sqlalchemy import literal_column
from decorators.session_decorator import with_session
from decorators.log_decorator import try_log

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__tablename__ = util.camel_to_snake(cls.__name__)

    @classmethod
    @with_session
    @try_log
    def batch_create(cls, data, update_fields=None, session=None):
        stmt = insert(cls).values(data)
        if update_fields is not None:
            update_dict = { field: literal_column(f"VALUES({field})") for field in update_fields }
            stmt = stmt.on_duplicate_key_update(**update_dict)
        session.execute(stmt)
    
    @classmethod
    @with_session
    @try_log
    def select(cls, *fields, session = None):
        return session.query(*fields)

    @classmethod
    @with_session
    def create(cls, session=None, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    @with_session
    def read(cls, session=None, **kwargs):
        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    @with_session
    def update(cls, filter_by, update_fields, session=None):
        session.query(cls).filter_by(**filter_by).update(update_fields)

    @classmethod
    @with_session
    def delete(cls, session=None, **kwargs):
        session.query(cls).filter_by(**kwargs).delete()