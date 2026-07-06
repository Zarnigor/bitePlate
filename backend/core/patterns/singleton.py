from threading import Lock
from typing import Any, Dict


class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass.
    Pattern #6: Singleton Pattern
    """

    _instances: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
