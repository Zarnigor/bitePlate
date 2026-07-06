from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Observer(ABC):
    """Abstract Observer — Pattern #2: Observer Pattern"""

    @abstractmethod
    def update(self, event: str, data: Dict[str, Any]) -> None:
        ...


class Subject:
    """
    Observable Subject — notifies all attached observers on state change.
    Pattern #2: Observer Pattern
    """

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(event, data)
