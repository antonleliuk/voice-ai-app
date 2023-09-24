from typing import Any

class SingletonMeta(type):
    _instances = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwds)
        return self._instances[self]