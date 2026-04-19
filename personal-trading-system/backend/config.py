"""
配置管理模块
"""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class SystemConfig(BaseSettings):
    """系统配置"""
    name: str = "个人量化交易系统"
    version: str = "1.0.0"
    debug: bool = False
    timezone: str = "Asia/Shanghai"
    data_dir: str = "../data"
    log_dir: str = "../logs"
    backup_dir: str = "../backups"


class SecurityConfig(BaseSettings):
    """安全配置"""
    master_key: str
    encryption_algorithm: str = "AES-GCM"
    key_derivation_iterations: int = 100000
    session_timeout: int = 3600


class RiskConfig(BaseSettings):
    """风控配置"""
    daily_loss_limit: float = 0.02  # 单日最大亏损2%
    max_position: float = 0.3       # 单币种最大仓位30%
    stop_loss: float = 0.05         # 止损5%
    take_profit: float = 0.10       # 止盈10%


class TradingConfig(BaseSettings):
    """交易配置"""
    default_exchange: str = "okx"
    mode: str = "paper"  # paper: 模拟交易, live: 实盘交易
    default_symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    risk: RiskConfig = RiskConfig()


class StrategyConfig(BaseSettings):
    """策略配置"""
    enabled: list[str] = ["ma_crossover", "rsi_reversion"]
    
    # 均线交叉策略
    ma_crossover_fast_period: int = 10
    ma_crossover_slow_period: int = 30
    ma_crossover_volume_threshold: float = 1.5
    
    # RSI回归策略
    rsi_reversion_period: int = 14
    rsi_reversion_oversold: int = 30
    rsi_reversion_overbought: int = 70
    rsi_reversion_exit: int = 50


class FeishuConfig(BaseSettings):
    """飞书配置"""
    enabled: bool = True
    webhook_url: Optional[str] = None
    notify_on: list[str] = ["order_filled", "system_error", "daily_report", "risk_warning"]


class NotificationConfig(BaseSettings):
    """通知配置"""
    enabled: bool = True
    feishu: FeishuConfig = FeishuConfig()


class DataConfig(BaseSettings):
    """数据配置"""
    storage_type: str = "sqlite"
    storage_path: str = "../data/trading.db"
    update_interval: int = 120  # 2分钟
    history_days: int = 30


class LoggingConfig(BaseSettings):
    """日志配置"""
    level: str = "INFO"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    rotation: str = "1 day"
    retention: str = "7 days"


class APIConfig(BaseSettings):
    """API配置"""
    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


class FrontendConfig(BaseSettings):
    """前端配置"""
    port: int = 3000
    title: str = "个人量化交易系统"


class Settings(BaseSettings):
    """全局配置"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    system: SystemConfig = SystemConfig()
    security: SecurityConfig
    trading: TradingConfig = TradingConfig()
    strategies: StrategyConfig = StrategyConfig()
    notifications: NotificationConfig = NotificationConfig()
    data: DataConfig = DataConfig()
    logging: LoggingConfig = LoggingConfig()
    api: APIConfig = APIConfig()
    frontend: FrontendConfig = FrontendConfig()


def load_yaml_config(config_path: str = "../config/settings.yaml") -> dict:
    """加载YAML配置文件"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        # 尝试加载示例配置
        example_file = Path("../config/settings.example.yaml")
        if example_file.exists():
            print(f"警告: 使用示例配置文件 {example_file}")
            config_file = example_file
        else:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_settings() -> Settings:
    """创建配置实例"""
    try:
        # 加载YAML配置
        yaml_config = load_yaml_config()
        
        # 合并环境变量和YAML配置
        config_dict = {}
        
        # 系统配置
        if 'system' in yaml_config:
            config_dict['system'] = SystemConfig(**yaml_config['system'])
        
        # 安全配置（必须从环境变量或YAML获取）
        if 'security' in yaml_config:
            config_dict['security'] = SecurityConfig(**yaml_config['security'])
        
        # 交易配置
        if 'trading' in yaml_config:
            trading_config = yaml_config['trading'].copy()
            if 'risk' in trading_config:
                trading_config['risk'] = RiskConfig(**trading_config['risk'])
            config_dict['trading'] = TradingConfig(**trading_config)
        
        # 策略配置
        if 'strategies' in yaml_config:
            strategies_config = yaml_config['strategies'].copy()
            config_dict['strategies'] = StrategyConfig(**strategies_config)
        
        # 通知配置
        if 'notifications' in yaml_config:
            notifications_config = yaml_config['notifications'].copy()
            if 'feishu' in notifications_config:
                notifications_config['feishu'] = FeishuConfig(**notifications_config['feishu'])
            config_dict['notifications'] = NotificationConfig(**notifications_config)
        
        # 数据配置
        if 'data' in yaml_config:
            config_dict['data'] = DataConfig(**yaml_config['data'])
        
        # 日志配置
        if 'logging' in yaml_config:
            config_dict['logging'] = LoggingConfig(**yaml_config['logging'])
        
        # API配置
        if 'api' in yaml_config:
            config_dict['api'] = APIConfig(**yaml_config['api'])
        
        # 前端配置
        if 'frontend' in yaml_config:
            config_dict['frontend'] = FrontendConfig(**yaml_config['frontend'])
        
        return Settings(**config_dict)
        
    except Exception as e:
        print(f"加载配置失败: {e}")
        print("使用默认配置...")
        # 使用默认配置，但安全配置必须提供
        security_config = SecurityConfig(
            master_key=os.getenv("MASTER_KEY", "default_master_key_change_me")
        )
        return Settings(security=security_config)


# 全局配置实例
settings = create_settings()


if __name__ == "__main__":
    # 测试配置加载
    print("系统配置:")
    print(f"  名称: {settings.system.name}")
    print(f"  版本: {settings.system.version}")
    print(f"  模式: {settings.trading.mode}")
    print(f"  交易所: {settings.trading.default_exchange}")
    print(f"  数据目录: {settings.system.data_dir}")