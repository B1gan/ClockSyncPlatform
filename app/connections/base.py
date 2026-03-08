"""连接抽象基类，统一不同协议连接的行为接口。"""
from abc import ABC, abstractmethod
from typing import Any


class BaseConnection(ABC):
    """协议连接的抽象基类，子类需实现 connect / disconnect / 等能力。"""

    def __init__(self, address: str | tuple[str, int]) -> None:
        if isinstance(address, str):
            self._address = address
            self._host, self._port = self._parse_address(address)
        else:
            self._host, self._port = address
            self._address = f"{address[0]}:{address[1]}"

    @staticmethod
    def _parse_address(address: str) -> tuple[str, int]:
        if ":" in address:
            host, port_str = address.rsplit(":", 1)
            return host.strip(), int(port_str.strip())
        return address.strip(), 123  # 默认 NTP 端口

    @property
    def address(self) -> str:
        return self._address

    @abstractmethod
    def connect(self) -> None:
        """建立连接。"""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """断开连接。"""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """是否已连接。"""
        ...

    def __enter__(self) -> "BaseConnection":
        self.connect()
        return self

    def __exit__(self, *args: Any) -> None:
        self.disconnect()
