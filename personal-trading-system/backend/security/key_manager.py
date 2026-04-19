"""
API密钥安全管理模块
使用主密钥加密存储交易所API密钥
"""

import base64
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from loguru import logger

from config import settings


class KeyManager:
    """API密钥管理器"""
    
    def __init__(self):
        self.master_key = settings.security.master_key.encode('utf-8')
        self.keys_file = Path(settings.system.data_dir) / "api_keys.enc"
        self.keys_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化加密器
        self.fernet = self._create_fernet()
        
        # 内存中的密钥缓存（使用时解密）
        self._key_cache: Dict[str, Dict[str, str]] = {}
        
        logger.info("密钥管理器初始化完成")
    
    def _create_fernet(self) -> Fernet:
        """创建Fernet加密器"""
        # 使用PBKDF2从主密钥派生加密密钥
        salt = b'personal_trading_system_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=settings.security.key_derivation_iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        return Fernet(key)
    
    def save_api_key(self, exchange: str, api_key: str, api_secret: str, 
                    passphrase: Optional[str] = None) -> bool:
        """
        保存API密钥（加密存储）
        
        Args:
            exchange: 交易所名称，如 'okx', 'binance'
            api_key: API Key
            api_secret: API Secret
            passphrase: 密码（某些交易所需要）
        
        Returns:
            bool: 是否保存成功
        """
        try:
            # 构建密钥数据
            key_data = {
                "api_key": api_key,
                "api_secret": api_secret,
            }
            if passphrase:
                key_data["passphrase"] = passphrase
            
            # 读取现有密钥
            all_keys = self._load_all_keys()
            
            # 更新指定交易所的密钥
            all_keys[exchange] = key_data
            
            # 加密并保存
            encrypted_data = self.fernet.encrypt(json.dumps(all_keys).encode('utf-8'))
            self.keys_file.write_bytes(encrypted_data)
            
            # 更新缓存
            self._key_cache[exchange] = key_data
            
            logger.info(f"已保存 {exchange} 的API密钥")
            return True
            
        except Exception as e:
            logger.error(f"保存API密钥失败: {e}")
            return False
    
    def get_api_key(self, exchange: str) -> Optional[Dict[str, str]]:
        """
        获取指定交易所的API密钥
        
        Args:
            exchange: 交易所名称
        
        Returns:
            Dict: 包含api_key, api_secret, passphrase的字典
        """
        # 检查缓存
        if exchange in self._key_cache:
            return self._key_cache[exchange].copy()
        
        try:
            # 从文件加载
            all_keys = self._load_all_keys()
            if exchange in all_keys:
                key_data = all_keys[exchange]
                # 缓存结果
                self._key_cache[exchange] = key_data.copy()
                return key_data
            
            logger.warning(f"未找到 {exchange} 的API密钥")
            return None
            
        except Exception as e:
            logger.error(f"获取API密钥失败: {e}")
            return None
    
    def delete_api_key(self, exchange: str) -> bool:
        """
        删除指定交易所的API密钥
        
        Args:
            exchange: 交易所名称
        
        Returns:
            bool: 是否删除成功
        """
        try:
            # 读取现有密钥
            all_keys = self._load_all_keys()
            
            if exchange not in all_keys:
                logger.warning(f"未找到 {exchange} 的API密钥")
                return False
            
            # 删除密钥
            del all_keys[exchange]
            
            # 如果还有密钥，保存；否则删除文件
            if all_keys:
                encrypted_data = self.fernet.encrypt(json.dumps(all_keys).encode('utf-8'))
                self.keys_file.write_bytes(encrypted_data)
            else:
                self.keys_file.unlink(missing_ok=True)
            
            # 清除缓存
            if exchange in self._key_cache:
                del self._key_cache[exchange]
            
            logger.info(f"已删除 {exchange} 的API密钥")
            return True
            
        except Exception as e:
            logger.error(f"删除API密钥失败: {e}")
            return False
    
    def list_exchanges(self) -> list[str]:
        """
        获取已配置的交易所列表
        
        Returns:
            list: 交易所名称列表
        """
        try:
            all_keys = self._load_all_keys()
            return list(all_keys.keys())
        except Exception as e:
            logger.error(f"获取交易所列表失败: {e}")
            return []
    
    def has_keys(self, exchange: Optional[str] = None) -> bool:
        """
        检查是否配置了API密钥
        
        Args:
            exchange: 指定交易所，如果为None则检查任意交易所
        
        Returns:
            bool: 是否配置了密钥
        """
        try:
            all_keys = self._load_all_keys()
            if exchange:
                return exchange in all_keys
            return len(all_keys) > 0
        except:
            return False
    
    def _load_all_keys(self) -> Dict[str, Dict[str, str]]:
        """加载所有加密的API密钥"""
        if not self.keys_file.exists():
            return {}
        
        try:
            encrypted_data = self.keys_file.read_bytes()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            logger.error(f"解密API密钥失败: {e}")
            return {}
    
    def change_master_key(self, new_master_key: str) -> bool:
        """
        更改主密钥（重新加密所有API密钥）
        
        Args:
            new_master_key: 新的主密钥
        
        Returns:
            bool: 是否更改成功
        """
        try:
            # 保存旧的主密钥
            old_master_key = self.master_key
            old_fernet = self.fernet
            
            # 加载所有密钥
            all_keys = self._load_all_keys()
            if not all_keys:
                logger.warning("没有需要重新加密的API密钥")
                return True
            
            # 更新主密钥
            self.master_key = new_master_key.encode('utf-8')
            self.fernet = self._create_fernet()
            
            # 重新加密并保存
            encrypted_data = self.fernet.encrypt(json.dumps(all_keys).encode('utf-8'))
            self.keys_file.write_bytes(encrypted_data)
            
            # 清除缓存
            self._key_cache.clear()
            
            logger.info("主密钥已更改，所有API密钥已重新加密")
            return True
            
        except Exception as e:
            # 恢复旧的主密钥
            self.master_key = old_master_key
            self.fernet = old_fernet
            logger.error(f"更改主密钥失败: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    # 创建测试实例
    key_manager = KeyManager()
    
    # 测试保存密钥
    test_exchange = "okx"
    test_api_key = "test_api_key_123"
    test_api_secret = "test_api_secret_456"
    
    print(f"保存 {test_exchange} 的API密钥...")
    success = key_manager.save_api_key(test_exchange, test_api_key, test_api_secret)
    print(f"保存结果: {'成功' if success else '失败'}")
    
    # 测试获取密钥
    print(f"\n获取 {test_exchange} 的API密钥...")
    keys = key_manager.get_api_key(test_exchange)
    if keys:
        print(f"API Key: {keys.get('api_key')}")
        print(f"API Secret: {keys.get('api_secret')}")
    else:
        print("获取失败")
    
    # 测试列出交易所
    print(f"\n已配置的交易所: {key_manager.list_exchanges()}")
    
    # 测试删除密钥
    print(f"\n删除 {test_exchange} 的API密钥...")
    success = key_manager.delete_api_key(test_exchange)
    print(f"删除结果: {'成功' if success else '失败'}")