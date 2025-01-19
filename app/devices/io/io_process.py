from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IoProcess(ABC, Generic[T]):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
