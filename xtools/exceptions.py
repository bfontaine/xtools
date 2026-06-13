from typing import Any

__all__ = ['BaseXToolsException', 'NotFound', 'TooManyEdits']


class BaseXToolsException(Exception):
    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BaseXToolsException) \
            and str(self) == str(other) \
            and self.code == other.code


class NotFound(BaseXToolsException):
    pass


class TooManyEdits(BaseXToolsException):
    pass
