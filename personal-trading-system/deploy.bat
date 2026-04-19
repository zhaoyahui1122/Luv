@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 个人量化交易系统部署脚本 (Windows)
REM 使用方法: deploy.bat [dev|prod]

set ENV=%1
if "%ENV%"=="" set ENV=dev

echo 🚀 开始部署个人量化交易系统 (%ENV% 环境)
set PROJECT_DIR=%~dp0
echo 项目目录: %PROJECT_DIR%

REM 检查环境
echo 🔍 检查环境...

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>nul') do set PYTHON_VERSION=%%i
echo ✅ Python !PYTHON_VERSION!

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js 未安装
    pause
    exit /b 1
)
for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js !NODE_VERSION!

REM 检查npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm 未安装
    pause
    exit /b 1
)
for /f %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✅ npm !NPM_VERSION!

REM 安装后端依赖
echo 📦 安装后端依赖...
cd /d "%PROJECT_DIR%backend"

REM 创建虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)

python -m pip install --upgrade pip
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ 后端依赖安装完成
) else (
    echo ❌ requirements.txt 不存在
    pause
    exit /b 1
)
deactivate

REM 安装前端依赖
echo 📦 安装前端依赖...
cd /d "%PROJECT_DIR%frontend"
if exist "package.json" (
    npm install
    echo ✅ 前端依赖安装完成
) else (
    echo ❌ package.json 不存在
    pause
    exit /b 1
)

REM 初始化配置
echo ⚙️ 初始化配置...

REM 创建必要的目录
if not exist "%PROJECT_DIR%data" mkdir "%PROJECT_DIR%data"
if not exist "%PROJECT_DIR%logs" mkdir "%PROJECT_DIR%logs"
if not exist "%PROJECT_DIR%backups" mkdir "%PROJECT_DIR%backups"

REM 复制配置文件
if not exist "%PROJECT_DIR%config\settings.yaml" (
    if exist "%PROJECT_DIR%config\settings.example.yaml" (
        copy "%PROJECT_DIR%config\settings.example.yaml" "%PROJECT_DIR%config\settings.yaml"
        echo 📝 已创建配置文件: config\settings.yaml
        echo ⚠️  请编辑配置文件并设置主密钥
    ) else (
        echo ❌ 配置文件模板不存在
        pause
        exit /b 1
    )
)

REM 构建前端
echo 🔨 构建前端...
cd /d "%PROJECT_DIR%frontend"
if "%ENV%"=="prod" (
    npm run build
    echo ✅ 前端生产构建完成
) else (
    echo ℹ️  开发环境跳过前端构建
)

echo.
echo 📊 部署完成!
echo ========================
echo 环境: %ENV%
echo 后端目录: %PROJECT_DIR%backend
echo 前端目录: %PROJECT_DIR%frontend
echo 数据目录: %PROJECT_DIR%data
echo 日志目录: %PROJECT_DIR%logs
echo.

if "%ENV%"=="dev" (
    echo 🎯 下一步:
    echo 1. 编辑配置文件: config\settings.yaml
    echo 2. 设置主密钥 (security.master_key)
    echo 3. 配置交易所API密钥
    echo 4. 按照下面的指示启动服务
    echo.
    echo 🚀 启动服务:
    echo 请打开两个命令提示符分别运行:
    echo 窗口1: 
    echo   cd %PROJECT_DIR%backend
    echo   venv\Scripts\activate
    echo   python main.py
    echo.
    echo 窗口2:
    echo   cd %PROJECT_DIR%frontend
    echo   npm run dev
)

echo.
echo ⚠️  安全提醒:
echo - 妥善保管主密钥
echo - 定期备份配置文件和数据
echo - 使用模拟交易充分测试
echo - 实盘交易前设置严格止损
echo.

pause