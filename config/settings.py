"""
TradingAgents 系统主配置文件

这个模块包含了系统的所有配置项，使用 Pydantic 进行类型验证和环境变量管理。
"""

from typing import Optional, List
from pydantic import BaseSettings, validator
from functools import lru_cache
import os


class DatabaseSettings(BaseSettings):
    """数据库配置"""
    
    url: str = "postgresql://postgres:password@localhost:5432/trading_agents"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False
    
    class Config:
        env_prefix = "DATABASE_"


class RedisSettings(BaseSettings):
    """Redis配置"""
    
    url: str = "redis://localhost:6379/0"
    password: Optional[str] = None
    db: int = 0
    max_connections: int = 10
    
    class Config:
        env_prefix = "REDIS_"


class LLMSettings(BaseSettings):
    """LLM模型配置"""
    
    # OpenAI配置
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.1
    
    # DeepSeek配置
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    
    # Anthropic配置
    anthropic_api_key: str = ""
    
    # 通用配置
    default_timeout: int = 30
    max_retries: int = 3
    
    class Config:
        env_prefix = ""


class DataSourceSettings(BaseSettings):
    """数据源配置"""
    
    tushare_token: str = ""
    alpha_vantage_api_key: str = ""
    yahoo_finance_enabled: bool = True
    
    # 数据更新配置
    market_data_update_interval: int = 60  # 秒
    news_data_update_interval: int = 300   # 秒
    
    class Config:
        env_prefix = ""


class SecuritySettings(BaseSettings):
    """安全配置"""
    
    secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    
    # API限流配置
    api_rate_limit: int = 100  # 每分钟请求数
    
    class Config:
        env_prefix = ""


class TradingSettings(BaseSettings):
    """交易配置"""
    
    trading_mode: str = "PAPER"  # PAPER 或 LIVE
    commission_rate: float = 0.001
    
    # 风控配置
    max_position_risk: float = 0.02    # 单笔交易最大风险2%
    max_portfolio_risk: float = 0.15   # 组合最大风险15%
    max_daily_loss: float = 0.05       # 最大日亏损5%
    
    # 仓位管理
    max_positions: int = 20
    default_position_size: float = 0.05  # 默认仓位大小5%
    
    class Config:
        env_prefix = "TRADING_"


class Settings(BaseSettings):
    """主配置类"""
    
    # 应用基础配置
    app_name: str = "TradingAgents"
    app_version: str = "1.0.0"
    debug: bool = False
    testing: bool = False
    log_level: str = "INFO"
    
    # 服务端口
    api_port: int = 8000
    web_port: int = 3000
    
    # 子配置
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    llm: LLMSettings = LLMSettings()
    data_source: DataSourceSettings = DataSourceSettings()
    security: SecuritySettings = SecuritySettings()
    trading: TradingSettings = TradingSettings()
    
    # Celery配置
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # 监控配置
    prometheus_port: int = 9090
    enable_metrics: bool = True
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'log_level must be one of {valid_levels}')
        return v.upper()
    
    @validator('trading_mode')
    def validate_trading_mode(cls, v):
        if v not in ['PAPER', 'LIVE']:
            raise ValueError('trading_mode must be either PAPER or LIVE')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（单例模式）"""
    return Settings()


# 全局配置实例
settings = get_settings()


def get_database_url() -> str:
    """获取数据库连接URL"""
    return settings.database.url


def get_redis_url() -> str:
    """获取Redis连接URL"""
    return settings.redis.url


def is_development() -> bool:
    """判断是否为开发环境"""
    return settings.debug


def is_testing() -> bool:
    """判断是否为测试环境"""
    return settings.testing 