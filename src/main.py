"""
TradingAgents 系统主入口

这是应用程序的主入口文件，负责初始化FastAPI应用、配置路由、中间件等。
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import uvicorn

from config.settings import get_settings
from config.database import init_db, check_db_connection
from config.redis import check_redis_connection

# 获取配置
settings = get_settings()

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动 TradingAgents 系统...")
    
    # 检查数据库连接
    if not check_db_connection():
        logger.error("❌ 数据库连接失败，请检查配置")
        raise RuntimeError("数据库连接失败")
    
    # 检查Redis连接
    if not check_redis_connection():
        logger.error("❌ Redis连接失败，请检查配置")
        raise RuntimeError("Redis连接失败")
    
    # 初始化数据库
    try:
        init_db()
        logger.info("✅ 数据库初始化完成")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        # 在开发环境可以继续，生产环境应该退出
        if not settings.debug:
            raise
    
    logger.info("✅ TradingAgents 系统启动完成")
    
    yield
    
    # 关闭时执行
    logger.info("🛑 关闭 TradingAgents 系统...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="基于多智能体LLM的智能股票筛选和交易系统",
    debug=settings.debug,
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加可信主机中间件（生产环境）
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
    )


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有HTTP请求"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "message": str(exc) if settings.debug else "服务暂时不可用",
            "path": str(request.url.path)
        }
    )


# 基础路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用 {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "debug": settings.debug
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    
    # 检查数据库连接
    db_status = check_db_connection()
    
    # 检查Redis连接
    redis_status = check_redis_connection()
    
    # 整体健康状态
    healthy = db_status and redis_status
    
    status_code = 200 if healthy else 503
    
    health_info = {
        "status": "healthy" if healthy else "unhealthy",
        "timestamp": time.time(),
        "services": {
            "database": "up" if db_status else "down",
            "redis": "up" if redis_status else "down"
        },
        "version": settings.app_version
    }
    
    return JSONResponse(content=health_info, status_code=status_code)


@app.get("/info")
async def app_info():
    """应用信息端点"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "environment": "development" if settings.debug else "production",
        "features": {
            "llm_enabled": bool(settings.llm.openai_api_key or settings.llm.deepseek_api_key),
            "trading_mode": settings.trading.trading_mode,
            "metrics_enabled": settings.enable_metrics
        }
    }


# 注册API路由
# 注意：这些路由模块需要在后续阶段创建
"""
from src.api.v1.routes import analysis, trading, portfolio, agents

app.include_router(
    analysis.router,
    prefix="/api/v1",
    tags=["analysis"]
)

app.include_router(
    trading.router,
    prefix="/api/v1",
    tags=["trading"]
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
    tags=["portfolio"]
)

app.include_router(
    agents.router,
    prefix="/api/v1",
    tags=["agents"]
)
"""


def create_app() -> FastAPI:
    """应用工厂函数"""
    return app


if __name__ == "__main__":
    # 直接运行时的配置
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=settings.debug
    ) 