"""
Redis缓存配置和管理
提供Redis连接、缓存管理和专用缓存类
"""

import redis
import json
import logging
from typing import Optional, Any, Dict, List

from .settings import get_settings

logger = logging.getLogger(__name__)

# 获取配置
settings = get_settings()

class RedisManager:
    """Redis连接管理器"""
    
    def __init__(self):
        self.client = None
        self._connect()
    
    def _connect(self):
        """建立Redis连接"""
        try:
            self.client = redis.from_url(
                settings.redis.url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # 测试连接
            self.client.ping()
            logger.info("Redis连接成功")
            
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            self.client = None
    
    def get_client(self):
        """获取Redis客户端"""
        if not self.client:
            self._connect()
        return self.client
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        try:
            if self.client:
                self.client.ping()
                return True
        except:
            pass
        return False

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置缓存"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            
            if expire:
                return self.redis.setex(key, expire, value)
            else:
                return self.redis.set(key, value)
        except Exception as e:
            logger.error(f"设置缓存失败 {key}: {e}")
            return False
    
    def get(self, key: str):
        """获取缓存"""
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            
            # 尝试JSON解析
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"获取缓存失败 {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"删除缓存失败 {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"检查缓存存在性失败 {key}: {e}")
            return False

def get_redis_client():
    """获取Redis客户端"""
    return redis_manager.get_client()

def check_redis_connection() -> bool:
    """检查Redis连接状态"""
    return redis_manager.is_connected()

# 全局实例
redis_manager = RedisManager()
cache_manager = CacheManager(redis_manager.get_client()) if redis_manager.get_client() else None

 