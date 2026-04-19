# 个人量化交易系统

> 安全、简洁、实用的个人量化交易工具

## 🎯 项目目标
- **个人使用**：专为个人交易者设计
- **安全第一**：保护API密钥和资金安全
- **实用为主**：满足日常交易需求
- **易于维护**：一个人能轻松维护

## 🏗️ 技术栈
- **后端**: FastAPI + SQLite + CCXT
- **前端**: React + TypeScript + Vite
- **安全**: 加密存储 + 本地优先
- **部署**: Docker + 本地运行

## 📁 项目结构
```
personal-trading-system/
├── backend/          # 后端服务
├── frontend/         # 前端界面
├── config/           # 配置文件（不提交Git）
├── data/             # 本地数据存储
├── logs/             # 系统日志
├── backups/          # 定期备份
└── README.md
```

## 🚀 快速开始

### 1. 环境准备
```bash
# Python 3.10+
python --version

# Node.js 18+
node --version
```

### 2. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

### 3. 配置系统
```bash
# 复制配置文件模板
cp config/settings.example.yaml config/settings.yaml
# 编辑配置文件，填入API密钥（加密存储）
```

### 4. 启动系统
```bash
# 启动后端
cd backend
python main.py

# 启动前端
cd ../frontend
npm run dev
```

访问 http://localhost:3000

## 🔐 安全特性
1. **API密钥加密存储** - 使用主密钥加密
2. **本地数据优先** - 敏感数据不离开本地
3. **权限最小化** - API只给交易权限
4. **定期备份** - 自动备份关键数据

## 📊 核心功能
- [ ] 交易所连接（OKX/币安等）
- [ ] API密钥安全管理
- [ ] 基础交易策略
- [ ] 风控系统
- [ ] 本地数据存储
- [ ] 飞书通知
- [ ] 每日盈亏报告

## ⚠️ 风险提示
量化交易存在极高风险，可能导致全部资金损失。建议：
1. 先用模拟账户测试
2. 小资金实盘验证
3. 设置严格止损
4. 定期审计交易记录

## 📝 开发计划
- **第一阶段**：基础框架搭建
- **第二阶段**：核心功能实现
- **第三阶段**：策略优化完善

## 📄 License
MIT