"""
数据库连接和会话管理
提供数据库连接池、会话管理和基础操作
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

from .settings import get_settings

logger = logging.getLogger(__name__)

# 获取配置
settings = get_settings()

# 创建数据库引擎
engine = create_engine(
    settings.database.url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.debug,
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基础模型类
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话（依赖注入用）
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话异常: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    获取数据库会话（上下文管理器）
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"数据库操作异常: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """
    初始化数据库表
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

def check_db_connection() -> bool:
    """
    检查数据库连接状态
    """
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        logger.info("数据库连接正常")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False

def close_db() -> None:
    """
    关闭数据库连接
    """
    try:
        engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {e}")

# 数据库事件监听器
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """设置数据库连接参数"""
    if "postgresql" in settings.database.url:
        # PostgreSQL特定设置
        with dbapi_connection.cursor() as cursor:
            cursor.execute("SET timezone TO 'UTC'")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """连接检出时的处理"""
    logger.debug("数据库连接已检出")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """连接检入时的处理"""
    logger.debug("数据库连接已检入") 