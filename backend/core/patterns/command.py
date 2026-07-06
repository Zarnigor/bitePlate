from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Abstract Command — Pattern #1: Command Pattern"""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        ...

    @abstractmethod
    def undo(self) -> None:
        """Reverse the command."""
        ...


class KitchenQueue:
    """
    Invoker — holds command history, supports execute/undo.
    Pattern #1: Command Pattern
    """

    def __init__(self) -> None:
        self._history: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            cmd = self._history.pop()
            cmd.undo()

    def clear(self) -> None:
        self._history.clear()

    @property
    def history_count(self) -> int:
        return len(self._history)
