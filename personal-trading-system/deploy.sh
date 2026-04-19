#!/bin/bash

# 个人量化交易系统部署脚本
# 使用方法: ./deploy.sh [dev|prod]

set -e

ENV=${1:-dev}
PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🚀 开始部署个人量化交易系统 ($ENV 环境)"
echo "项目目录: $PROJECT_DIR"

# 检查环境
check_environment() {
    echo "🔍 检查环境..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $PYTHON_VERSION"
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装"
        exit 1
    fi
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION"
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        echo "❌ npm 未安装"
        exit 1
    fi
    NPM_VERSION=$(npm --version)
    echo "✅ npm $NPM_VERSION"
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 未安装"
        exit 1
    fi
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo "✅ pip $PIP_VERSION"
}

# 安装后端依赖
install_backend() {
    echo "📦 安装后端依赖..."
    cd "$PROJECT_DIR/backend"
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        echo "✅ 后端依赖安装完成"
    else
        echo "❌ requirements.txt 不存在"
        exit 1
    fi
    
    deactivate
}

# 安装前端依赖
install_frontend() {
    echo "📦 安装前端依赖..."
    cd "$PROJECT_DIR/frontend"
    
    if [ -f "package.json" ]; then
        npm install
        echo "✅ 前端依赖安装完成"
    else
        echo "❌ package.json 不存在"
        exit 1
    fi
}

# 初始化配置
init_config() {
    echo "⚙️ 初始化配置..."
    
    # 创建必要的目录
    mkdir -p "$PROJECT_DIR/data"
    mkdir -p "$PROJECT_DIR/logs"
    mkdir -p "$PROJECT_DIR/backups"
    
    # 复制配置文件
    if [ ! -f "$PROJECT_DIR/config/settings.yaml" ]; then
        if [ -f "$PROJECT_DIR/config/settings.example.yaml" ]; then
            cp "$PROJECT_DIR/config/settings.example.yaml" "$PROJECT_DIR/config/settings.yaml"
            echo "📝 已创建配置文件: config/settings.yaml"
            echo "⚠️  请编辑配置文件并设置主密钥"
        else
            echo "❌ 配置文件模板不存在"
            exit 1
        fi
    fi
    
    # 设置文件权限
    chmod 600 "$PROJECT_DIR/config/settings.yaml" 2>/dev/null || true
}

# 构建前端
build_frontend() {
    echo "🔨 构建前端..."
    cd "$PROJECT_DIR/frontend"
    
    if [ "$ENV" = "prod" ]; then
        npm run build
        echo "✅ 前端生产构建完成"
    else
        echo "ℹ️  开发环境跳过前端构建"
    fi
}

# 启动服务
start_services() {
    echo "🚀 启动服务..."
    
    case $ENV in
        "dev")
            echo "开发模式启动..."
            echo "1. 后端: http://localhost:8000"
            echo "2. 前端: http://localhost:3000"
            echo ""
            echo "请打开两个终端分别运行:"
            echo "终端1: cd $PROJECT_DIR/backend && source venv/bin/activate && python main.py"
            echo "终端2: cd $PROJECT_DIR/frontend && npm run dev"
            ;;
        "prod")
            echo "生产模式启动..."
            # 这里可以添加生产环境启动脚本
            # 例如使用gunicorn + nginx
            echo "生产环境部署需要额外配置"
            ;;
        *)
            echo "❌ 未知环境: $ENV"
            echo "用法: $0 [dev|prod]"
            exit 1
            ;;
    esac
}

# 显示系统信息
show_info() {
    echo ""
    echo "📊 部署完成!"
    echo "========================"
    echo "环境: $ENV"
    echo "后端目录: $PROJECT_DIR/backend"
    echo "前端目录: $PROJECT_DIR/frontend"
    echo "数据目录: $PROJECT_DIR/data"
    echo "日志目录: $PROJECT_DIR/logs"
    echo ""
    
    if [ "$ENV" = "dev" ]; then
        echo "🎯 下一步:"
        echo "1. 编辑配置文件: config/settings.yaml"
        echo "2. 设置主密钥 (security.master_key)"
        echo "3. 配置交易所API密钥"
        echo "4. 按照上面的指示启动服务"
    fi
    
    echo ""
    echo "⚠️  安全提醒:"
    echo "- 妥善保管主密钥"
    echo "- 定期备份配置文件和数据"
    echo "- 使用模拟交易充分测试"
    echo "- 实盘交易前设置严格止损"
}

# 主流程
main() {
    check_environment
    install_backend
    install_frontend
    init_config
    build_frontend
    start_services
    show_info
}

# 执行主流程
main