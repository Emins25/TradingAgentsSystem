"""
Redis配置和连接管理

这个模块负责Redis连接的创建、管理和维护，提供缓存操作的封装。
"""

import redis
import json
from typing import Any, Optional, Dict, Union
from contextlib import contextmanager
from datetime import timedelta
import logging

from config.settings import get_settings

# 获取配置
settings = get_settings()

# 配置日志
logger = logging.getLogger(__name__)


class RedisManager:
    """Redis管理器"""
    
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """建立Redis连接"""
        try:
            # 解析Redis URL
            self.redis_client = redis.from_url(
                settings.redis.url,
                max_connections=settings.redis.max_connections,
                decode_responses=True,  # 自动解码响应
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis连接成功")
            
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            raise
    
    def get_client(self) -> redis.Redis:
        """获取Redis客户端"""
        if not self.redis_client:
            self._connect()
        return self.redis_client
    
    def ping(self) -> bool:
        """检查Redis连接"""
        try:
            return self.redis_client.ping()
        except Exception as e:
            logger.error(f"Redis ping失败: {e}")
            return False
    
    def close(self):
        """关闭Redis连接"""
        if self.redis_client:
            self.redis_client.close()


# 全局Redis管理器实例
redis_manager = RedisManager()


def get_redis_client() -> redis.Redis:
    """获取Redis客户端实例"""
    return redis_manager.get_client()


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.client = get_redis_client()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒）
            
        Returns:
            bool: 是否设置成功
        """
        try:
            # 序列化值
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            elif not isinstance(value, str):
                value = str(value)
            
            if ttl:
                return self.client.setex(key, ttl, value)
            else:
                return self.client.set(key, value)
                
        except Exception as e:
            logger.error(f"缓存设置失败 key={key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            Any: 缓存值，不存在时返回None
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            
            # 尝试反序列化JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error(f"缓存获取失败 key={key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否删除成功
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"缓存删除失败 key={key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        检查缓存是否存在
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否存在
        """
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"缓存检查失败 key={key}: {e}")
            return False
    
    def expire(self, key: str, ttl: int) -> bool:
        """
        设置缓存过期时间
        
        Args:
            key: 缓存键
            ttl: 过期时间（秒）
            
        Returns:
            bool: 是否设置成功
        """
        try:
            return bool(self.client.expire(key, ttl))
        except Exception as e:
            logger.error(f"缓存过期时间设置失败 key={key}: {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """
        获取缓存剩余过期时间
        
        Args:
            key: 缓存键
            
        Returns:
            int: 剩余时间（秒），-1表示永不过期，-2表示不存在
        """
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"获取缓存TTL失败 key={key}: {e}")
            return -2
    
    def clear_pattern(self, pattern: str) -> int:
        """
        删除匹配模式的缓存
        
        Args:
            pattern: 匹配模式，如 "user:*"
            
        Returns:
            int: 删除的键数量
        """
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"批量删除缓存失败 pattern={pattern}: {e}")
            return 0


# 全局缓存管理器实例
cache_manager = CacheManager()


class MarketDataCache:
    """市场数据缓存"""
    
    def __init__(self):
        self.cache = cache_manager
        self.prefix = "market_data"
    
    def set_stock_price(self, symbol: str, data: Dict[str, Any], ttl: int = 300):
        """缓存股票价格数据"""
        key = f"{self.prefix}:price:{symbol}"
        return self.cache.set(key, data, ttl)
    
    def get_stock_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取股票价格数据"""
        key = f"{self.prefix}:price:{symbol}"
        return self.cache.get(key)
    
    def set_technical_indicators(self, symbol: str, indicators: Dict[str, Any], ttl: int = 600):
        """缓存技术指标数据"""
        key = f"{self.prefix}:indicators:{symbol}"
        return self.cache.set(key, indicators, ttl)
    
    def get_technical_indicators(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取技术指标数据"""
        key = f"{self.prefix}:indicators:{symbol}"
        return self.cache.get(key)


class AnalysisCache:
    """分析结果缓存"""
    
    def __init__(self):
        self.cache = cache_manager
        self.prefix = "analysis"
    
    def set_analysis_result(self, symbol: str, analyst_type: str, result: Dict[str, Any], ttl: int = 1800):
        """缓存分析结果"""
        key = f"{self.prefix}:{analyst_type}:{symbol}"
        return self.cache.set(key, result, ttl)
    
    def get_analysis_result(self, symbol: str, analyst_type: str) -> Optional[Dict[str, Any]]:
        """获取分析结果"""
        key = f"{self.prefix}:{analyst_type}:{symbol}"
        return self.cache.get(key)


# 专用缓存管理器实例
market_data_cache = MarketDataCache()
analysis_cache = AnalysisCache()


def check_redis_connection() -> bool:
    """检查Redis连接状态"""
    return redis_manager.ping()


def get_redis_info() -> Dict[str, Any]:
    """获取Redis连接信息"""
    client = get_redis_client()
    try:
        info = client.info()
        return {
            "redis_version": info.get('redis_version'),
            "connected_clients": info.get('connected_clients'),
            "used_memory_human": info.get('used_memory_human'),
            "keyspace": info.get('db0', {}),
        }
    except Exception as e:
        logger.error(f"获取Redis信息失败: {e}")
        return {} 