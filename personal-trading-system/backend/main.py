#!/usr/bin/env python3
"""
个人量化交易系统 - 后端主程序
"""

import asyncio
import signal
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from security.key_manager import KeyManager
from trading.engine import TradingEngine
from database import init_db
from scheduler import Scheduler
from logger import setup_logger

# 初始化日志
logger = setup_logger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.system.name,
    version=settings.system.version,
    description="个人量化交易系统后端API"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局实例
key_manager = None
trading_engine = None
scheduler = None


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    global key_manager, trading_engine, scheduler
    
    logger.info(f"启动 {settings.system.name} v{settings.system.version}")
    
    try:
        # 初始化数据库
        await init_db()
        logger.info("数据库初始化完成")
        
        # 初始化密钥管理器
        key_manager = KeyManager()
        logger.info("密钥管理器初始化完成")
        
        # 初始化交易引擎
        trading_engine = TradingEngine(key_manager)
        logger.info("交易引擎初始化完成")
        
        # 初始化调度器
        scheduler = Scheduler(trading_engine)
        await scheduler.start()
        logger.info("调度器启动完成")
        
        logger.info("系统启动完成，准备就绪")
        
    except Exception as e:
        logger.error(f"启动失败: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("正在关闭系统...")
    
    if scheduler:
        await scheduler.stop()
        logger.info("调度器已停止")
    
    if trading_engine:
        await trading_engine.stop()
        logger.info("交易引擎已停止")
    
    logger.info("系统关闭完成")


@app.get("/")
async def root():
    """根路径，返回系统信息"""
    return {
        "name": settings.system.name,
        "version": settings.system.version,
        "status": "running",
        "mode": settings.trading.mode,
        "exchange": settings.trading.default_exchange
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time()
    }


@app.get("/api/v1/status")
async def get_system_status():
    """获取系统状态"""
    if not trading_engine:
        raise HTTPException(status_code=503, detail="交易引擎未就绪")
    
    status = await trading_engine.get_status()
    return status


@app.post("/api/v1/engine/start")
async def start_engine():
    """启动交易引擎"""
    if not trading_engine:
        raise HTTPException(status_code=503, detail="交易引擎未就绪")
    
    await trading_engine.start()
    return {"message": "交易引擎已启动", "status": "running"}


@app.post("/api/v1/engine/stop")
async def stop_engine():
    """停止交易引擎"""
    if not trading_engine:
        raise HTTPException(status_code=503, detail="交易引擎未就绪")
    
    await trading_engine.stop()
    return {"message": "交易引擎已停止", "status": "stopped"}


def signal_handler(signum, frame):
    """信号处理函数"""
    logger.info(f"收到信号 {signum}，正在优雅关闭...")
    sys.exit(0)


if __name__ == "__main__":
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动服务器
    logger.info(f"启动服务器: {settings.api.host}:{settings.api.port}")
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.system.debug,
        log_level="info" if settings.system.debug else "warning"
    )