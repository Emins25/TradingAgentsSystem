#!/usr/bin/env python3
"""
开发环境设置脚本

这个脚本帮助开发者快速设置TradingAgents的开发环境。
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 11):
        print("❌ Python版本必须是3.11或更高")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def check_docker():
    """检查Docker是否安装"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker未安装或不在PATH中")
    return False

def check_docker_compose():
    """检查Docker Compose是否安装"""
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker Compose未安装或不在PATH中")
    return False

def create_env_file():
    """创建.env文件"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✅ .env文件已存在")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ 从.env.example创建了.env文件")
        print("⚠️  请编辑.env文件，填入相应的API密钥")
        return True
    else:
        # 创建基本的.env文件
        env_content = """# TradingAgents 环境变量配置
DEBUG=True
LOG_LEVEL=INFO

# 数据库配置
DATABASE_URL=postgresql://postgres:password@localhost:5432/trading_agents

# Redis配置
REDIS_URL=redis://localhost:6379/0

# LLM API配置 (请填入您的API密钥)
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 数据源配置
TUSHARE_TOKEN=your_tushare_token_here

# 安全配置
SECRET_KEY=change-this-secret-key-in-production
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ 创建了基本的.env文件")
        print("⚠️  请编辑.env文件，填入相应的API密钥")
        return True

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Python依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def start_docker_services():
    """启动Docker服务"""
    print("🐳 启动Docker服务...")
    try:
        subprocess.run(['docker-compose', 'up', '-d', 'db', 'redis'], check=True)
        print("✅ Docker服务启动成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker服务启动失败: {e}")
        return False

def test_configuration():
    """测试配置"""
    print("🧪 测试配置...")
    try:
        # 测试导入配置
        sys.path.insert(0, str(Path.cwd()))
        from config.settings import get_settings
        settings = get_settings()
        print(f"✅ 配置加载成功: {settings.app_name} v{settings.app_version}")
        
        # 测试数据库连接
        from config.database import check_db_connection
        if check_db_connection():
            print("✅ 数据库连接测试成功")
        else:
            print("⚠️  数据库连接测试失败，请检查Docker服务是否启动")
        
        # 测试Redis连接
        from config.redis import check_redis_connection
        if check_redis_connection():
            print("✅ Redis连接测试成功")
        else:
            print("⚠️  Redis连接测试失败，请检查Docker服务是否启动")
            
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 TradingAgents 开发环境设置")
    print("=" * 50)
    
    checks = [
        ("Python版本检查", check_python_version),
        ("Docker检查", check_docker),
        ("Docker Compose检查", check_docker_compose),
    ]
    
    # 执行检查
    for name, check_func in checks:
        if not check_func():
            print(f"\n❌ {name}失败，请解决后重试")
            return False
    
    print("\n📝 设置开发环境...")
    
    setup_steps = [
        ("创建环境变量文件", create_env_file),
        ("安装Python依赖", install_dependencies),
        ("启动Docker服务", start_docker_services),
        ("测试配置", test_configuration),
    ]
    
    # 执行设置步骤
    for name, setup_func in setup_steps:
        print(f"\n{name}...")
        if not setup_func():
            print(f"❌ {name}失败")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 开发环境设置完成！")
    print("\n下一步:")
    print("1. 编辑 .env 文件，填入您的API密钥")
    print("2. 运行 'python src/main.py' 启动服务")
    print("3. 访问 http://localhost:8000 查看API文档")
    print("4. 访问 http://localhost:8000/health 检查服务状态")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 