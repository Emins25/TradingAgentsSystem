# TradingAgents System

基于多智能体大语言模型(LLM)的智能股票筛选和交易系统

## 📖 项目概述

TradingAgents是一个创新的智能交易系统，通过模拟真实交易公司的组织架构和协作模式，利用多个专业化的LLM智能体进行协作决策。系统整合基本面、技术面、情绪面和新闻面分析，实现股票筛选、分析和交易决策的自动化。

### 🎯 核心价值

- **多维度分析能力**：整合基本面、技术面、情绪面、新闻面分析
- **协作决策机制**：通过多智能体辩论和协作提高决策质量  
- **风险控制优先**：内置多层次风险管理机制
- **高度可扩展性**：支持多种LLM模型和交易策略的灵活配置

## 🏗️ 系统架构

### 智能体团队结构

```
┌─────────────────────────────────────────────────────────────┐
│                    TradingAgents 系统架构                      │
├─────────────────────────────────────────────────────────────┤
│  I. 分析师团队 (Analyst Team)                                   │
│  ├─ 基本面分析师 (Fundamental Analyst)                         │
│  ├─ 情绪分析师 (Sentiment Analyst)                             │
│  ├─ 新闻分析师 (News Analyst)                                  │
│  └─ 技术分析师 (Technical Analyst)                             │
├─────────────────────────────────────────────────────────────┤
│  II. 研究团队 (Research Team)                                  │
│  ├─ 看涨研究员 (Bullish Researcher)                           │
│  ├─ 看跌研究员 (Bearish Researcher)                           │
│  └─ 辩论协调员 (Debate Facilitator)                           │
├─────────────────────────────────────────────────────────────┤
│  III. 交易员 (Trader)                                         │
│  └─ 交易决策执行                                              │
├─────────────────────────────────────────────────────────────┤
│  IV. 风险管理团队 (Risk Management Team)                       │
│  ├─ 风险偏好型分析师 (Risky Analyst)                           │
│  ├─ 中性分析师 (Neutral Analyst)                              │
│  ├─ 保守型分析师 (Safe Analyst)                               │
│  └─ 风险协调员 (Risk Facilitator)                             │
├─────────────────────────────────────────────────────────────┤
│  V. 基金经理 (Fund Manager)                                   │
│  └─ 最终决策审批                                              │
└─────────────────────────────────────────────────────────────┘
```

### 技术架构

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

## ✨ 功能特性

### 核心功能

- **多维度数据分析**
  - 基本面数据：财务报表、盈利数据、公司公告
  - 技术面数据：价格、成交量、60+技术指标
  - 情绪面数据：社交媒体情绪、新闻情绪
  - 宏观数据：经济指标、政策变化、市场事件

- **智能体协作机制**
  - 结构化通信协议
  - 多轮辩论机制
  - 信息状态管理
  - 决策权重分配

- **交易决策引擎**
  - 基于多智能体共识的决策
  - 风险约束下的仓位管理
  - 时机选择优化
  - 止损止盈策略

- **风险管理系统**
  - 实时风险监控
  - 多层次风险控制
  - 压力测试
  - 合规检查

### 辅助功能

- **数据管理**：多源数据集成、数据清洗、历史回测
- **性能监控**：收益率分析、风险指标、夏普比率
- **可视化界面**：投资组合概览、决策过程可视化

## 🛠️ 技术栈

### 后端技术

- **框架**: Python + FastAPI
- **LLM集成**: OpenAI API、DeepSeek API
- **数据库**: PostgreSQL (关系型) + Redis (缓存)
- **消息队列**: Redis Pub/Sub
- **数据源**: Tushare、Yahoo Finance、Alpha Vantage

### 前端技术

- **框架**: React + TypeScript
- **状态管理**: Redux Toolkit
- **图表库**: Chart.js / D3.js
- **UI组件**: Ant Design

### 部署技术

- **容器化**: Docker + Docker Compose
- **编排**: Kubernetes
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 本地开发环境搭建

1. **克隆项目**
```bash
git clone https://github.com/your-repo/TradingAgentsSystem.git
cd TradingAgentsSystem
```

2. **安装后端依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，配置API密钥和数据库连接
```

4. **启动数据库服务**
```bash
docker-compose up -d db redis
```

5. **运行数据库迁移**
```bash
python -m alembic upgrade head
```

6. **启动后端服务**
```bash
python -m uvicorn src.main:app --reload
```

7. **安装前端依赖并启动**
```bash
cd web
npm install
npm start
```

### Docker部署

```bash
# 使用Docker Compose一键启动所有服务
docker-compose up -d

# 访问应用
# Web界面: http://localhost:3000
# API文档: http://localhost:8000/docs
```

## 📁 项目结构

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

## 📊 性能目标

### 交易性能
- **累计收益率**：目标超越基准指数10-20%
- **夏普比率**：目标大于1.5
- **最大回撤**：控制在15%以内
- **胜率**：目标达到55%以上

### 技术性能
- **响应时间**：单次决策<5分钟
- **数据处理能力**：支持同时分析50+股票
- **系统可用性**：99.5%的正常运行时间
- **并发处理**：支持多个交易策略并行运行

## 🛡️ 风险管理

### 交易风险控制
- 设置最大单日亏损限制
- 实施动态止损机制
- 多样化投资组合
- 定期压力测试

### 技术风险控制
- API调用失败重试机制
- 模型输出验证
- 数据质量监控
- 系统故障自动恢复

### 合规风险管理
- 遵循金融监管要求
- 交易记录完整保存
- 内幕交易检测
- 市场操纵预防

## 🔧 开发指南

### 代码规范
- 使用Python 3.11+
- 遵循PEP 8代码风格
- 使用类型注解
- 单元测试覆盖率85%+

### Git工作流
- 使用GitFlow分支策略
- main分支用于生产环境
- develop分支用于开发环境

### 测试
```bash
# 运行单元测试
python -m pytest tests/unit

# 运行集成测试
python -m pytest tests/integration

# 运行端到端测试
python -m pytest tests/e2e

# 生成测试覆盖率报告
python -m pytest --cov=src tests/
```

## 📚 文档

- [架构设计文档](./TradingAgents_Architecture_Design.md)
- [工程结构设计](./Engineering_Structure.md)  
- [产品需求文档](./TradingAgents_PRD.md)
- [API文档](http://localhost:8000/docs)

## 🚀 部署指南

### 生产环境部署

1. **准备环境**
```bash
# 克隆项目
git clone https://github.com/your-repo/TradingAgentsSystem.git
cd TradingAgentsSystem

# 配置生产环境变量
cp .env.example .env.prod
# 编辑生产环境配置
```

2. **Docker部署**
```bash
# 构建并启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker-compose ps
```

3. **Kubernetes部署**
```bash
# 应用Kubernetes配置
kubectl apply -f deploy/k8s/

# 查看部署状态
kubectl get pods
kubectl get services
```

### 监控和维护

- **监控面板**: http://localhost:3000/grafana
- **日志查看**: `docker-compose logs -f`
- **健康检查**: http://localhost:8000/health

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 贡献要求
- 遵循代码规范
- 添加相应的测试
- 更新相关文档
- 通过CI/CD检查

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- [项目主页](https://github.com/your-repo/TradingAgentsSystem)
- [问题反馈](https://github.com/your-repo/TradingAgentsSystem/issues)
- [讨论区](https://github.com/your-repo/TradingAgentsSystem/discussions)

## 📞 联系我们

- 邮箱: contact@tradingagents.com
- 微信群: [加入微信群]
- QQ群: [加入QQ群]

---

**⚠️ 免责声明**

本系统仅用于研究和教育目的。任何基于本系统做出的投资决策所产生的收益或损失，均由用户自行承担。请在充分了解市场风险的前提下谨慎投资。

**版本**: 1.0.0  
**最后更新**: 2024年  
**维护状态**: 积极维护