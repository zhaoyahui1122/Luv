"""
日志配置模块
"""

import sys
from pathlib import Path
from loguru import logger

from config import settings


def setup_logger(name: str = __name__):
    """配置日志系统"""
    
    # 移除默认处理器
    logger.remove()
    
    # 日志目录
    log_dir = Path(settings.system.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件路径
    log_file = log_dir / "trading.log"
    error_log_file = log_dir / "error.log"
    
    # 控制台输出格式
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 文件输出格式
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # 添加控制台处理器
    logger.add(
        sys.stderr,
        format=console_format,
        level=settings.logging.level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # 添加普通日志文件处理器
    logger.add(
        log_file,
        format=file_format,
        level=settings.logging.level,
        rotation=settings.logging.rotation,
        retention=settings.logging.retention,
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )
    
    # 添加错误日志文件处理器（只记录ERROR及以上）
    logger.add(
        error_log_file,
        format=file_format,
        level="ERROR",
        rotation=settings.logging.rotation,
        retention=settings.logging.retention,
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )
    
    # 返回配置好的logger
    return logger.bind(name=name)


# 全局日志实例
log = setup_logger("trading_system")


class TradingLogger:
    """交易专用日志记录器"""
    
    @staticmethod
    def order_placed(order_id: str, symbol: str, side: str, amount: float, price: float):
        """记录订单创建"""
        log.info(f"订单创建 | ID: {order_id} | {symbol} | {side} | 数量: {amount} | 价格: {price}")
    
    @staticmethod
    def order_filled(order_id: str, symbol: str, side: str, amount: float, price: float, fee: float = 0):
        """记录订单成交"""
        log.info(f"订单成交 | ID: {order_id} | {symbol} | {side} | 数量: {amount} | 价格: {price} | 手续费: {fee}")
    
    @staticmethod
    def order_cancelled(order_id: str, symbol: str, reason: str = ""):
        """记录订单取消"""
        log.info(f"订单取消 | ID: {order_id} | {symbol} | 原因: {reason}")
    
    @staticmethod
    def strategy_signal(strategy: str, symbol: str, signal: str, confidence: float = 0):
        """记录策略信号"""
        log.info(f"策略信号 | {strategy} | {symbol} | 信号: {signal} | 置信度: {confidence:.2f}")
    
    @staticmethod
    def risk_warning(level: str, message: str, data: dict = None):
        """记录风险警告"""
        log.warning(f"风险警告 | 级别: {level} | {message}" + (f" | 数据: {data}" if data else ""))
    
    @staticmethod
    def profit_loss(symbol: str, pnl: float, pnl_percent: float, total_pnl: float):
        """记录盈亏"""
        pnl_type = "盈利" if pnl >= 0 else "亏损"
        log.info(f"盈亏记录 | {symbol} | {pnl_type}: ${pnl:.2f} ({pnl_percent:.2%}) | 总盈亏: ${total_pnl:.2f}")
    
    @staticmethod
    def system_event(event: str, details: str = ""):
        """记录系统事件"""
        log.info(f"系统事件 | {event}" + (f" | {details}" if details else ""))
    
    @staticmethod
    def error_event(error_type: str, error_msg: str, context: dict = None):
        """记录错误事件"""
        log.error(f"错误事件 | 类型: {error_type} | 消息: {error_msg}" + (f" | 上下文: {context}" if context else ""))


# 测试代码
if __name__ == "__main__":
    log.info("日志系统测试 - 普通信息")
    log.warning("日志系统测试 - 警告信息")
    log.error("日志系统测试 - 错误信息")
    
    # 测试交易日志
    trading_log = TradingLogger()
    trading_log.order_placed("12345", "BTC/USDT", "buy", 0.01, 45000.50)
    trading_log.order_filled("12345", "BTC/USDT", "buy", 0.01, 45000.00, 0.001)
    trading_log.strategy_signal("ma_crossover", "BTC/USDT", "BUY", 0.85)
    trading_log.risk_warning("medium", "接近止损线", {"current_price": 44000, "stop_loss": 43500})
    trading_log.profit_loss("BTC/USDT", 150.25, 0.033, 3250.75)
    
    print(f"\n日志文件位置: {log_dir.absolute()}")
    print("日志配置完成")