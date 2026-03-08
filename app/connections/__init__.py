"""连接层：多协议连接抽象与工厂创建。"""
from app.connections.base import BaseConnection
from app.connections.factory import ConnectionFactory
from app.connections.ntp_connection import NTPConnection
from app.connections.ptp_connection import PTPConnection

__all__ = [
    "BaseConnection",
    "NTPConnection",
    "PTPConnection",
    "ConnectionFactory",
]
