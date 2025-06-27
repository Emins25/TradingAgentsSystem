"""
TradingAgents 系统配置管理
统一管理所有配置项，支持环境变量覆盖
"""

from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings
import os

class DatabaseSettings(BaseSettings):
    """数据库配置"""
    host: str = Field(default="localhost", description="数据库主机")
    port: int = Field(default=5432, description="数据库端口")
    username: str = Field(default="postgres", description="数据库用户名")
    password: str = Field(default="password", description="数据库密码")
    database: str = Field(default="trading_agents", description="数据库名")
    
    @property
    def url(self) -> str:
        """获取数据库连接URL"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "DB_"

class RedisSettings(BaseSettings):
    """Redis配置"""
    host: str = Field(default="localhost", description="Redis主机")
    port: int = Field(default=6379, description="Redis端口")
    password: Optional[str] = Field(default=None, description="Redis密码")
    db: int = Field(default=0, description="Redis数据库编号")
    
    @property
    def url(self) -> str:
        """获取Redis连接URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
    
    class Config:
        env_prefix = "REDIS_"

class LLMSettings(BaseSettings):
    """LLM配置"""
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API密钥")
    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API基础URL")
    deepseek_api_key: Optional[str] = Field(default=None, description="DeepSeek API密钥")
    deepseek_base_url: str = Field(default="https://api.deepseek.com/v1", description="DeepSeek API基础URL")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API密钥")
    
    # 模型配置
    default_model: str = Field(default="gpt-3.5-turbo", description="默认使用的模型")
    max_tokens: int = Field(default=4000, description="最大token数")
    temperature: float = Field(default=0.7, description="温度参数")
    
    class Config:
        env_prefix = "LLM_"

class DataSourceSettings(BaseSettings):
    """数据源配置"""
    tushare_token: Optional[str] = Field(default=None, description="Tushare API令牌")
    yahoo_finance_enabled: bool = Field(default=True, description="是否启用Yahoo Finance")
    alpha_vantage_key: Optional[str] = Field(default=None, description="Alpha Vantage API密钥")
    
    # 数据更新频率（分钟）
    realtime_update_interval: int = Field(default=1, description="实时数据更新间隔")
    daily_update_time: str = Field(default="18:00", description="日线数据更新时间")
    
    class Config:
        env_prefix = "DATA_"

class SecuritySettings(BaseSettings):
    """安全配置"""
    secret_key: str = Field(default="your-secret-key-change-in-production", description="JWT密钥")
    algorithm: str = Field(default="HS256", description="JWT算法")
    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间（分钟）")
    
    # API限流
    rate_limit_per_minute: int = Field(default=100, description="每分钟API调用限制")
    
    class Config:
        env_prefix = "SECURITY_"

class LoggingSettings(BaseSettings):
    """日志配置"""
    level: str = Field(default="INFO", description="日志级别")
    format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        description="日志格式"
    )
    file_rotation: str = Field(default="100 MB", description="日志文件轮转大小")
    file_retention: str = Field(default="30 days", description="日志文件保留时间")
    
    class Config:
        env_prefix = "LOG_"

class TradingSettings(BaseSettings):
    """交易配置"""
    # 风险控制
    max_position_size: float = Field(default=0.1, description="单个持仓最大比例")
    max_daily_loss: float = Field(default=0.05, description="单日最大亏损比例")
    stop_loss_threshold: float = Field(default=0.08, description="止损阈值")
    
    # 交易时间
    market_open_time: str = Field(default="09:30", description="开市时间")
    market_close_time: str = Field(default="15:00", description="收市时间")
    
    # 策略参数
    analysis_lookback_days: int = Field(default=30, description="分析回看天数")
    min_confidence_score: float = Field(default=0.6, description="最小置信度分数")
    
    class Config:
        env_prefix = "TRADING_"

class Settings(BaseSettings):
    """主配置类"""
    # 应用基础配置
    app_name: str = Field(default="TradingAgents", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    environment: str = Field(default="development", description="运行环境")
    
    # 各模块配置
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    data_source: DataSourceSettings = Field(default_factory=DataSourceSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    trading: TradingSettings = Field(default_factory=TradingSettings)
    
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'testing', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'Environment must be one of {allowed}')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# 全局配置实例
settings = Settings()

def get_settings() -> Settings:
    """获取配置实例"""
    return settings

def reload_settings():
    """重新加载配置"""
    global settings
    settings = Settings()
    return settings 