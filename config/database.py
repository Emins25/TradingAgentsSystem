"""
数据库配置和连接管理

这个模块负责数据库连接的创建、管理和维护，包括连接池配置、会话管理等。
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

from config.settings import get_settings

# 获取配置
settings = get_settings()

# 创建数据库引擎
engine = create_engine(
    settings.database.url,
    poolclass=QueuePool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_pre_ping=True,  # 连接前检查连接是否有效
    pool_recycle=3600,   # 连接回收时间
    echo=settings.database.echo,  # 是否打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ORM基类
Base = declarative_base()

# 元数据
metadata = MetaData()

# 配置日志
logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    这是一个依赖注入函数，用于在FastAPI路由中获取数据库会话。
    会话会在请求结束后自动关闭。
    
    Yields:
        Session: SQLAlchemy数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话出错: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    获取数据库会话的上下文管理器
    
    用于在非FastAPI环境中获取数据库会话，支持事务管理。
    
    Yields:
        Session: SQLAlchemy数据库会话
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"数据库事务失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    初始化数据库
    
    创建所有表结构。这个函数应该在应用启动时调用一次。
    """
    try:
        # 导入所有模型，确保它们被注册到Base.metadata中
        from src.models.database import stock_models, news_models, trade_models
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


def check_db_connection() -> bool:
    """
    检查数据库连接是否正常
    
    Returns:
        bool: 连接是否正常
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("数据库连接正常")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False


def get_db_info() -> dict:
    """
    获取数据库信息
    
    Returns:
        dict: 数据库连接信息
    """
    return {
        "url": settings.database.url.split('@')[1] if '@' in settings.database.url else settings.database.url,
        "pool_size": settings.database.pool_size,
        "max_overflow": settings.database.max_overflow,
        "echo": settings.database.echo,
    }


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_all_tables(self):
        """创建所有表"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_all_tables(self):
        """删除所有表（谨慎使用）"""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return SessionLocal()
    
    def execute_raw_sql(self, sql: str):
        """执行原生SQL"""
        with self.engine.connect() as connection:
            return connection.execute(sql)


# 全局数据库管理器实例
db_manager = DatabaseManager() 