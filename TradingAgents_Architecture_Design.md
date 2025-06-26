# TradingAgents 系统架构设计文档

## 1. 架构概述

### 1.1 架构原则
- **模块化设计**：各智能体独立封装，便于维护和扩展
- **松耦合**：通过标准化接口和消息协议实现组件间通信
- **高可用性**：支持容错机制和故障恢复
- **可扩展性**：支持水平扩展和新智能体的动态添加
- **安全性**：多层安全防护和权限控制

### 1.2 技术栈选择
- **后端框架**：Python + FastAPI
- **LLM集成**：OpenAI API、DeepSeek API
- **数据库**：PostgreSQL (关系型) + Redis (缓存)
- **消息队列**：Redis Pub/Sub
- **数据获取**：Tushare、Yahoo Finance、Alpha Vantage
- **Web框架**：React + TypeScript
- **部署**：Docker + Docker Compose

## 2. 系统整体架构

### 2.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    表示层 (Presentation Layer)                │
├─────────────────────────────────────────────────────────────┤
│  Web Interface  │  REST API  │  WebSocket  │  Dashboard     │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    业务逻辑层 (Business Layer)                 │
├─────────────────────────────────────────────────────────────┤
│           智能体编排器 (Agent Orchestrator)                   │
├─────────────────────────────────────────────────────────────┤
│  分析师团队  │  研究团队  │  交易员  │  风控  │  基金经理      │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    服务层 (Service Layer)                     │
├─────────────────────────────────────────────────────────────┤
│  通信协议  │  状态管理  │  决策引擎  │  风险监控  │  执行引擎  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    数据层 (Data Layer)                        │
├─────────────────────────────────────────────────────────────┤
│  数据获取  │  数据处理  │  数据存储  │  缓存管理  │  指标计算  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件架构

```
                    ┌─────────────────┐
                    │   Web Frontend  │
                    └─────────┬───────┘
                              │ HTTPS/WebSocket
                    ┌─────────▼───────┐
                    │   API Gateway   │
                    └─────────┬───────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼────────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Agent Manager  │ │ Data Hub  │ │Risk Engine│
    └───────┬────────┘ └─────┬─────┘ └─────┬─────┘
            │                │               │
    ┌───────▼────────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Communication  │ │PostgreSQL │ │  Redis    │
    │   Protocol     │ │ Database  │ │  Cache    │
    └────────────────┘ └───────────┘ └───────────┘
```

## 3. 智能体系统架构

### 3.1 智能体基础架构

```python
class BaseAgent:
    """智能体基础类"""
    def __init__(self, agent_id: str, role: str, config: dict):
        self.agent_id = agent_id
        self.role = role
        self.config = config
        self.state = AgentState()
        self.memory = AgentMemory()
        self.llm_client = LLMClient(config)
        
    def process(self, input_data: dict) -> dict:
        """核心处理逻辑"""
        pass
        
    def communicate(self, message: Message, target: str):
        """智能体间通信"""
        pass
```

### 3.2 分析师团队架构

```
┌─────────────────────────────────────────────────────────────┐
│                    分析师团队 (Analyst Team)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────│
│  │ Fundamental │  │ Sentiment   │  │    News     │  │Technical│
│  │  Analyst    │  │  Analyst    │  │  Analyst    │  │ Analyst │
│  └─────┬───────┘  └─────┬───────┘  └─────┬───────┘  └─────┬─│
│        │ 财务数据        │ 情绪数据        │ 新闻数据        │ 技术│
│        ▼                ▼                ▼                ▼ │
│  ┌─────────────────────────────────────────────────────────┐│
│  │            Analysis Report Aggregator                   ││
│  │               (分析报告聚合器)                            ││
│  └─────────────────────┬───────────────────────────────────┘│
└────────────────────────┼────────────────────────────────────┘
                         ▼
                 ┌──────────────┐
                 │ Global State │
                 │  (全局状态)   │
                 └──────────────┘
```

### 3.3 通信协议架构

```python
class CommunicationProtocol:
    """通信协议"""
    
    @dataclass
    class Message:
        sender: str
        receiver: str
        message_type: str  # 'report', 'debate', 'decision'
        content: dict
        timestamp: datetime
        priority: int
        
    @dataclass 
    class GlobalState:
        market_data: dict
        analysis_reports: dict
        debate_history: list
        decisions: list
        risk_metrics: dict
        portfolio_state: dict
```

## 4. 数据架构设计

### 4.1 数据流架构

```
External APIs                Data Processing              Storage
     │                            │                         │
┌────▼────┐    ┌──────────┐   ┌───▼────┐   ┌──────────┐  ┌─▼─┐
│Tushare  │───▶│Data      │──▶│Data    │──▶│Data      │─▶│DB │
│API      │    │Collector │   │Cleaner │   │Validator │  │   │
└─────────┘    └──────────┘   └────────┘   └──────────┘  └───┘
┌─────────┐    ┌──────────┐   ┌────────┐   ┌──────────┐  ┌─▼─┐
│Yahoo    │───▶│Real-time │──▶│Format  │──▶│Index     │─▶│   │
│Finance  │    │Fetcher   │   │Normaliz│   │Builder   │  │   │
└─────────┘    └──────────┘   └────────┘   └──────────┘  └───┘
┌─────────┐    ┌──────────┐   ┌────────┐   ┌──────────┐  ┌─▼─┐
│News API │───▶│Sentiment │──▶│NLP     │──▶│Feature   │─▶│   │
│Sources  │    │Analyzer  │   │Process │   │Extractor │  │   │
└─────────┘    └──────────┘   └────────┘   └──────────┘  └───┘
```

### 4.2 数据库设计

```sql
-- 股票基础信息表
CREATE TABLE stocks (
    symbol VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sector VARCHAR(50),
    industry VARCHAR(50),
    market_cap BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 历史价格数据表
CREATE TABLE historical_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(10,4),
    high_price DECIMAL(10,4),
    low_price DECIMAL(10,4),
    close_price DECIMAL(10,4),
    volume BIGINT,
    adjusted_close DECIMAL(10,4),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol),
    UNIQUE(symbol, date)
);

-- 技术指标表
CREATE TABLE technical_indicators (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    indicator_name VARCHAR(50) NOT NULL,
    indicator_value DECIMAL(15,6),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol),
    INDEX idx_symbol_date (symbol, date)
);

-- 新闻数据表
CREATE TABLE news_data (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    source VARCHAR(100),
    published_at TIMESTAMP,
    sentiment_score DECIMAL(3,2),
    symbols TEXT[], -- 相关股票代码数组
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 智能体决策记录表
CREATE TABLE agent_decisions (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    decision_type VARCHAR(20), -- 'buy', 'sell', 'hold'
    confidence_score DECIMAL(3,2),
    reasoning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);

-- 交易记录表
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    trade_type VARCHAR(10), -- 'buy', 'sell'
    quantity INTEGER NOT NULL,
    price DECIMAL(10,4) NOT NULL,
    total_amount DECIMAL(15,4),
    commission DECIMAL(10,4),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);
```

## 5. 微服务架构设计

### 5.1 服务拆分

```
┌─────────────────────────────────────────────────────────────┐
│                     微服务架构图                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    API       │  │    Agent     │  │    Data      │     │
│  │   Gateway    │  │   Manager    │  │   Service    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │             │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐     │
│  │  Analysis    │  │ Communication│  │ Market Data  │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Risk Manager │  │ Trade Engine │  │ Notification │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 服务详细设计

#### 5.2.1 API Gateway Service
```python
# api_gateway/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="TradingAgents API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/analysis/start")
async def start_analysis(request: AnalysisRequest):
    # 触发分析流程
    pass

@app.get("/api/v1/portfolio/status")
async def get_portfolio_status():
    # 获取投资组合状态
    pass
```

#### 5.2.2 Agent Manager Service
```python
# agent_manager/main.py
class AgentManager:
    def __init__(self):
        self.agents = {}
        self.orchestrator = AgentOrchestrator()
        
    async def create_agent(self, agent_config: dict):
        """创建智能体实例"""
        agent = AgentFactory.create_agent(agent_config)
        self.agents[agent.agent_id] = agent
        return agent
        
    async def execute_workflow(self, workflow_config: dict):
        """执行智能体工作流"""
        return await self.orchestrator.execute(workflow_config)
```

#### 5.2.3 Data Service
```python
# data_service/main.py
class DataService:
    def __init__(self):
        self.collectors = {
            'tushare': TushareCollector(),
            'yahoo': YahooFinanceCollector(),
            'news': NewsCollector()
        }
        
    async def fetch_market_data(self, symbols: list, timeframe: str):
        """获取市场数据"""
        tasks = []
        for symbol in symbols:
            task = self.collectors['tushare'].fetch_data(symbol, timeframe)
            tasks.append(task)
        return await asyncio.gather(*tasks)
        
    async def fetch_news_data(self, keywords: list, timeframe: str):
        """获取新闻数据"""
        return await self.collectors['news'].fetch_news(keywords, timeframe)
```

## 6. 部署架构

### 6.1 Docker容器化

```yaml
# docker-compose.yml
version: '3.8'

services:
  api-gateway:
    build: ./api_gateway
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/trading_agents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  agent-manager:
    build: ./agent_manager
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/trading_agents
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    depends_on:
      - db
      - redis

  data-service:
    build: ./data_service
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/trading_agents
      - TUSHARE_TOKEN=${TUSHARE_TOKEN}
    depends_on:
      - db

  risk-manager:
    build: ./risk_manager
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/trading_agents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  web-frontend:
    build: ./web_frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=trading_agents
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 6.2 Kubernetes部署

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trading-agents-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trading-agents-api
  template:
    metadata:
      labels:
        app: trading-agents-api
    spec:
      containers:
      - name: api-gateway
        image: trading-agents/api-gateway:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: database-url
        - name: REDIS_URL
          value: "redis://redis-service:6379"
```

## 7. 安全架构

### 7.1 安全层次

```
┌─────────────────────────────────────────────────────────────┐
│                    安全防护层次                              │
├─────────────────────────────────────────────────────────────┤
│ 网络安全层    │ WAF │ DDoS防护 │ SSL/TLS │ VPN        │    │
├─────────────────────────────────────────────────────────────┤
│ 应用安全层    │ JWT │ OAuth2.0 │ RBAC   │ 输入验证    │    │
├─────────────────────────────────────────────────────────────┤
│ 数据安全层    │ 加密存储 │ 备份 │ 脱敏   │ 审计日志    │    │
├─────────────────────────────────────────────────────────────┤
│ 接口安全层    │ API限流 │ 签名 │ 防重放  │ 权限控制    │    │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 认证授权设计

```python
# security/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt

class AuthManager:
    def __init__(self):
        self.secret_key = "your-secret-key"
        self.algorithm = "HS256"
        
    def create_token(self, user_data: dict) -> str:
        """创建JWT令牌"""
        payload = {
            "user_id": user_data["user_id"],
            "role": user_data["role"],
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
    def verify_token(self, token: str) -> dict:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

# 权限装饰器
def require_permission(permission: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 权限检查逻辑
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 8. 监控和日志架构

### 8.1 监控系统

```
┌─────────────────────────────────────────────────────────────┐
│                    监控架构                                  │
├─────────────────────────────────────────────────────────────┤
│ 业务监控      │ 交易性能 │ 决策准确率 │ 风险指标 │ 用户行为  │
├─────────────────────────────────────────────────────────────┤
│ 应用监控      │ API响应时间 │ 错误率 │ 吞吐量 │ 资源使用   │
├─────────────────────────────────────────────────────────────┤
│ 基础设施监控   │ CPU │ 内存 │ 磁盘 │ 网络 │ 数据库性能     │
├─────────────────────────────────────────────────────────────┤
│ 日志收集      │ ELK Stack │ 结构化日志 │ 分布式追踪       │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 日志设计

```python
# logging/logger.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_agent_action(self, agent_id: str, action: str, data: dict):
        """记录智能体行为"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "data": data,
            "level": "INFO"
        }
        self.logger.info(json.dumps(log_data))
        
    def log_trade_execution(self, trade_data: dict):
        """记录交易执行"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "trade_execution",
            "trade_data": trade_data,
            "level": "INFO"
        }
        self.logger.info(json.dumps(log_data))
```

## 9. 性能优化策略

### 9.1 缓存策略

```python
# cache/strategy.py
from redis import Redis
import json

class CacheManager:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379, db=0)
        
    def cache_market_data(self, symbol: str, data: dict, ttl: int = 300):
        """缓存市场数据"""
        key = f"market_data:{symbol}"
        self.redis_client.setex(key, ttl, json.dumps(data))
        
    def cache_analysis_result(self, symbol: str, analyst_type: str, result: dict, ttl: int = 600):
        """缓存分析结果"""
        key = f"analysis:{analyst_type}:{symbol}"
        self.redis_client.setex(key, ttl, json.dumps(result))
        
    def get_cached_data(self, key: str):
        """获取缓存数据"""
        data = self.redis_client.get(key)
        return json.loads(data) if data else None
```

### 9.2 异步处理

```python
# async/processor.py
import asyncio
from celery import Celery

# Celery配置
celery_app = Celery(
    'trading_agents',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def process_market_data_async(symbol: str, timeframe: str):
    """异步处理市场数据"""
    # 数据处理逻辑
    pass

@celery_app.task
def run_analysis_pipeline(symbols: list):
    """异步运行分析流水线"""
    # 分析流水线逻辑
    pass

class AsyncTaskManager:
    @staticmethod
    async def schedule_daily_analysis():
        """调度每日分析任务"""
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
        tasks = []
        for symbol in symbols:
            task = process_market_data_async.delay(symbol, "1d")
            tasks.append(task)
        return tasks
```

## 10. 扩展性设计

### 10.1 插件化架构

```python
# plugins/interface.py
from abc import ABC, abstractmethod

class AnalystPlugin(ABC):
    """分析师插件接口"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
        
    @abstractmethod
    def analyze(self, data: dict) -> dict:
        pass
        
    @abstractmethod
    def get_config_schema(self) -> dict:
        pass

class DataSourcePlugin(ABC):
    """数据源插件接口"""
    
    @abstractmethod
    def fetch_data(self, symbol: str, timeframe: str) -> dict:
        pass
        
    @abstractmethod
    def get_supported_symbols(self) -> list:
        pass

# 插件管理器
class PluginManager:
    def __init__(self):
        self.plugins = {}
        
    def register_plugin(self, plugin_type: str, plugin: ABC):
        """注册插件"""
        if plugin_type not in self.plugins:
            self.plugins[plugin_type] = []
        self.plugins[plugin_type].append(plugin)
        
    def get_plugins(self, plugin_type: str) -> list:
        """获取插件列表"""
        return self.plugins.get(plugin_type, [])
```

---

**文档版本**：1.0  
**创建日期**：2024年  
**作者**：AI Assistant  
**状态**：设计阶段 