"""NTP 协议连接实现。"""
from app.connections.base import BaseConnection


class NTPConnection(BaseConnection):
    """NTP 协议连接，用于与 NTP 设备或服务端通信。"""

    def __init__(self, address: str | tuple[str, int]) -> None:
        super().__init__(address)
        self._connected = False

    def connect(self) -> None:
        # 实际可接入 ntplib 等库与 NTP 服务器建连
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected
