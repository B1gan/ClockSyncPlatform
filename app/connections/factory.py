"""连接工厂：根据协议类型创建对应连接实例，扩展新协议只需注册，无需改调用方。"""
from typing import Callable, TypeAlias

from app.connections.base import BaseConnection
from app.connections.ntp_connection import NTPConnection
from app.connections.ptp_connection import PTPConnection

Address: TypeAlias = str | tuple[str, int]
ConnectionConstructor: TypeAlias = Callable[[Address], BaseConnection]


class ConnectionFactory:
    """根据 protocol 创建对应连接实例；新协议通过 register 扩展。"""

    _registry: dict[str, ConnectionConstructor] = {}

    @classmethod
    def register(cls, protocol: str) -> Callable[[ConnectionConstructor], ConnectionConstructor]:
        """注册协议：用 @ConnectionFactory.register("xxx") 装饰连接类或构造函数。"""

        def decorator(factory: ConnectionConstructor) -> ConnectionConstructor:
            cls._registry[protocol.lower()] = factory
            return factory

        return decorator

    @classmethod
    def create_connection(cls, protocol: str, address: Address) -> BaseConnection:
        """
        根据 protocol 创建连接实例。
        :param protocol: 协议标识，如 "ntp", "ptp"
        :param address: 地址，如 "192.168.1.1:123" 或 ("192.168.1.1", 123)
        :return: 对应协议的连接实例
        :raises ValueError: 未注册的 protocol
        """
        key = protocol.lower().strip()
        if key not in cls._registry:
            raise ValueError(f"未知协议: {protocol}，已注册: {list(cls._registry.keys())}")
        return cls._registry[key](address)

    @classmethod
    def supported_protocols(cls) -> list[str]:
        """返回当前支持的协议列表。"""
        return list(cls._registry.keys())


# 注册内置协议，后续新协议只需在此处或通过 register 装饰器添加
ConnectionFactory.register("ntp")(lambda addr: NTPConnection(addr))
ConnectionFactory.register("ptp")(lambda addr: PTPConnection(addr))
