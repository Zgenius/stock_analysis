from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.setting import DATABASE_URL
import logging

# 加载环境变量
engine = create_engine(
    DATABASE_URL,
    pool_size=100,          # 增加连接池大小
    max_overflow=50,       # 增加允许溢出的连接数
    pool_timeout=30,       # 连接池超时时间
    pool_recycle=1800      # 连接回收时间
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SessionManager:
    @staticmethod
    @contextmanager
    def get_session():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            logging.info("Session closed")