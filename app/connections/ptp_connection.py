"""PTP 协议连接实现。"""
from app.connections.base import BaseConnection


class PTPConnection(BaseConnection):
    """PTP 协议连接，用于与 PTP 设备或主钟通信。"""

    def __init__(self, address: str | tuple[str, int]) -> None:
        super().__init__(address)
        self._connected = False

    def connect(self) -> None:
        # 实际可接入 ptp 库或硬件接口
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected
