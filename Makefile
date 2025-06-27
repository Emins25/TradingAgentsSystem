# TradingAgents 项目 Makefile
.PHONY: help install dev test lint format clean build docker-build docker-up docker-down

# 默认目标
help:
	@echo "TradingAgents 开发工具"
	@echo ""
	@echo "可用命令:"
	@echo "  install     - 安装项目依赖"
	@echo "  dev         - 安装开发依赖"
	@echo "  test        - 运行测试"
	@echo "  lint        - 代码检查"
	@echo "  format      - 代码格式化"
	@echo "  clean       - 清理临时文件"
	@echo "  build       - 构建项目"
	@echo "  docker-build - 构建Docker镜像"
	@echo "  docker-up   - 启动Docker服务"
	@echo "  docker-down - 停止Docker服务"
	@echo "  run         - 启动开发服务器"
	@echo "  db-init     - 初始化数据库"
	@echo "  db-migrate  - 数据库迁移"
	@echo "  db-upgrade  - 升级数据库"

# 安装基本依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
dev:
	pip install -e ".[dev]"
	pre-commit install

# 运行测试
test:
	pytest tests/ -v --cov=src --cov=config --cov-report=html --cov-report=term

# 运行单元测试
test-unit:
	pytest tests/unit -v

# 运行集成测试
test-integration:
	pytest tests/integration -v

# 代码检查
lint:
	flake8 src config tests
	mypy src config
	black --check src config tests
	isort --check-only src config tests

# 代码格式化
format:
	black src config tests
	isort src config tests

# 清理临时文件
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# 构建项目
build:
	python -m build

# 启动开发服务器
run:
	python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 启动生产服务器
run-prod:
	python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker相关命令
docker-build:
	docker build -t trading-agents:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

# 仅启动数据库服务
docker-db:
	docker-compose up -d db redis

# 数据库相关命令
db-init:
	python -c "from config.database import init_db; init_db()"

db-migrate:
	alembic revision --autogenerate -m "Auto migration"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	docker-compose down -v
	docker-compose up -d db redis
	sleep 5
	make db-upgrade

# Celery相关命令
celery-worker:
	celery -A src.background.scheduler worker --loglevel=info

celery-beat:
	celery -A src.background.scheduler beat --loglevel=info

celery-flower:
	celery -A src.background.scheduler flower --port=5555

# 监控相关命令
monitor-up:
	docker-compose --profile monitoring up -d

monitor-down:
	docker-compose --profile monitoring down

# 环境设置
setup-env:
	@if [ ! -f .env ]; then \
		echo "创建 .env 文件..."; \
		cp .env.example .env; \
		echo "请编辑 .env 文件，填入相应的配置"; \
	else \
		echo ".env 文件已存在"; \
	fi

# 检查环境
check-env:
	@echo "检查Python版本..."
	@python --version
	@echo "检查pip版本..."
	@pip --version
	@echo "检查Docker版本..."
	@docker --version
	@echo "检查Docker Compose版本..."
	@docker-compose --version

# 完整的开发环境设置
setup: setup-env install dev docker-db
	@echo "开发环境设置完成！"
	@echo "请确保已正确配置 .env 文件中的API密钥"

# 安全检查
security:
	pip-audit
	safety check

# 生成requirements.txt（从pyproject.toml）
freeze:
	pip-compile pyproject.toml --output-file requirements.txt

# 更新依赖
update:
	pip-compile --upgrade pyproject.toml --output-file requirements.txt
	pip install -r requirements.txt

# 项目信息
info:
	@echo "项目名称: TradingAgents"
	@echo "版本: 1.0.0"
	@echo "Python版本: $(shell python --version)"
	@echo "项目路径: $(shell pwd)"
	@echo "虚拟环境: $(VIRTUAL_ENV)" 