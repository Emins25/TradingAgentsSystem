# TradingAgents 工程结构设计文档

基于《TradingAgents_Architecture_Design.md》的架构设计，本文档详细规划了整个TradingAgents系统的工程结构和实现方案。

## 1. 项目目录结构

```
TradingAgentsSystem/
├── README.md                          # 项目说明文档
├── requirements.txt                   # Python依赖包
├── docker-compose.yml                 # Docker编排文件
├── Dockerfile                         # Docker镜像构建文件
├── .env.example                       # 环境变量示例
├── .gitignore                         # Git忽略文件
├── pyproject.toml                     # Python项目配置
├── Makefile                           # 构建和部署脚本
│
├── docs/                              # 文档目录
│   ├── api/                          # API文档
│   ├── deployment/                   # 部署文档
│   └── user_guide/                   # 用户指南
│
├── config/                           # 配置文件目录
│   ├── settings.py                   # 主配置文件
│   ├── database.py                   # 数据库配置
│   ├── redis.py                      # Redis配置
│   └── llm_models.py                 # LLM模型配置
│
├── src/                              # 源代码目录
│   ├── main.py                       # 应用入口
│   │
│   ├── agents/                       # 智能体模块
│   │   ├── base/                     # 基础智能体
│   │   ├── analysts/                 # 分析师团队
│   │   ├── researchers/              # 研究团队
│   │   ├── trader/                   # 交易员
│   │   ├── risk_management/          # 风险管理团队
│   │   └── fund_manager/             # 基金经理
│   │
│   ├── core/                         # 核心模块
│   │   ├── communication/            # 通信协议
│   │   ├── llm/                      # LLM集成
│   │   ├── security/                 # 安全模块
│   │   └── utils/                    # 工具模块
│   │
│   ├── data/                         # 数据模块
│   │   ├── sources/                  # 数据源
│   │   ├── processors/               # 数据处理
│   │   ├── indicators/               # 技术指标
│   │   └── storage/                  # 数据存储
│   │
│   ├── api/                          # API层
│   │   ├── v1/routes/               # 路由定义
│   │   ├── v1/schemas/              # 数据模型
│   │   └── middleware/               # 中间件
│   │
│   ├── models/                       # 数据模型
│   │   ├── database/                 # 数据库模型
│   │   └── business/                 # 业务模型
│   │
│   ├── services/                     # 服务层
│   │   ├── market_data_service.py    # 市场数据服务
│   │   ├── analysis_service.py       # 分析服务
│   │   ├── trading_service.py        # 交易服务
│   │   └── risk_service.py           # 风险服务
│   │
│   └── background/                   # 后台任务
│       ├── scheduler.py              # 任务调度器
│       ├── data_collector.py         # 数据收集任务
│       └── analysis_runner.py        # 分析运行任务
│
├── tests/                            # 测试目录
│   ├── unit/                         # 单元测试
│   ├── integration/                  # 集成测试
│   └── e2e/                         # 端到端测试
│
├── web/                              # 前端代码
│   ├── src/                          # 源代码
│   ├── public/                       # 静态资源
│   └── dist/                         # 构建输出
│
├── database/                         # 数据库相关
│   ├── migrations/                   # 数据库迁移
│   ├── seeds/                        # 种子数据
│   └── schemas/                      # 数据库架构
│
└── deploy/                           # 部署配置
    ├── docker/                       # Docker配置
    ├── k8s/                         # Kubernetes配置
    └── nginx/                        # Nginx配置
```

## 2. 核心模块设计

### 2.1 智能体基础架构

```python
# src/agents/base/agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentState:
    """智能体状态"""
    agent_id: str
    status: str  # 'idle', 'processing', 'waiting', 'error'
    last_action: Optional[str] = None
    last_update: datetime = datetime.utcnow()

class BaseAgent(ABC):
    """智能体基础类"""
    
    def __init__(self, agent_id: str, role: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.role = role
        self.config = config
        self.state = AgentState(agent_id=agent_id, status='idle')
        self.llm_client = self._init_llm_client()
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入数据，返回处理结果"""
        pass
        
    @abstractmethod
    def get_prompt_template(self) -> str:
        """获取提示词模板"""
        pass
```

### 2.2 通信协议设计

```python
# src/core/communication/protocol.py
@dataclass
class Message:
    """消息数据结构"""
    id: str
    sender: str
    receiver: str
    type: str  # 'request', 'response', 'broadcast'
    content: Dict[str, Any]
    timestamp: datetime

class CommunicationProtocol:
    """智能体通信协议"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        
    async def publish_message(self, channel: str, message: Message):
        """发布消息到指定频道"""
        pass
        
    async def subscribe_channel(self, channel: str, callback):
        """订阅频道消息"""
        pass
```

## 3. API设计

### 3.1 API路由结构

```python
# src/api/v1/routes/analysis.py
from fastapi import APIRouter, Depends
from typing import List
from ...schemas.analysis import AnalysisRequest, AnalysisResponse

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/start", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest):
    """启动股票分析流程"""
    pass

@router.get("/status/{task_id}")
async def get_analysis_status(task_id: str):
    """获取分析任务状态"""
    pass
```

### 3.2 数据模型

```python
# src/api/v1/schemas/analysis.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    symbols: List[str]
    analysis_types: List[str] = ["fundamental", "technical", "sentiment"]
    timeframe: str = "1d"

class AnalysisResponse(BaseModel):
    task_id: str
    status: str
    message: str
    estimated_completion: Optional[datetime] = None
```

## 4. 配置管理

### 4.1 主配置文件

```python
# config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "TradingAgents"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost/trading_agents"
    
    # LLM API配置
    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    
    # 数据源配置
    TUSHARE_TOKEN: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 5. 部署配置

### 5.1 Docker配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/trading_agents
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=trading_agents
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## 6. 开发规范

### 6.1 代码规范
- 使用Python 3.11+
- 遵循PEP 8代码风格
- 使用类型注解
- 单元测试覆盖率85%+

### 6.2 Git工作流
- 使用GitFlow分支策略
- main分支用于生产环境
- develop分支用于开发环境

### 6.3 依赖管理

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
redis==5.0.1
pandas==2.1.4
openai==1.3.7
tushare==1.2.89
pytest==7.4.3
```

## 7. 启动指南

### 7.1 开发环境搭建

```bash
# 克隆项目
git clone https://github.com/Emins25/TradingAgentsSystem.git

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 启动服务
python -m uvicorn src.main:app --reload
```

---

**文档版本**：1.0  
**创建日期**：2024年  
**作者**：AI Assistant 