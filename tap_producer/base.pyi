from contextlib import AbstractContextManager
from types import TracebackType
from typing import Callable
from typing import ClassVar
from typing import ContextManager
from typing import Counter
from typing import NoReturn
from typing import Protocol
from typing import TextIO
from typing import runtime_checkable

FormatWarningType = Callable[[Warning | str, type[Warning], str, int, str | None], str]
ShowWarningType = Callable[[Warning | str, type[Warning], str, int, TextIO | None, str | None], None]

@runtime_checkable
class _LockType(AbstractContextManager[bool], Protocol):
    def acquire(self, blocking: bool = ..., timeout: float = ...) -> bool: ...
    def release(self) -> None: ...

@runtime_checkable
class _TestAnything(AbstractContextManager[_TestAnything], Protocol):
    """Static type for the TAP-Producer context decorator."""
    _formatwarning: ClassVar[FormatWarningType]
    _showwarning: ClassVar[ShowWarningType]
    _count: ClassVar[Counter[str]]
    _version: ClassVar[int]
    __lock: ClassVar[_LockType]
    __plan: int | None
    __version: int | None
    def __init__(self: _TestAnything, plan: int | None = None, version: int | None = None) -> None: ...
    def __enter__(self: _TestAnything) -> _TestAnything: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None: ...
    @classmethod
    def version(cls: type[_TestAnything], version: int = ...) -> type[_TestAnything]: ...
    @classmethod
    def plan(cls: type[_TestAnything], count: int | None = None, skip_reason: str = '', skip_count: int | None = None) -> type[_TestAnything]: ...
    @classmethod
    def ok(cls: type[_TestAnything], *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> type[_TestAnything]: ...
    @classmethod
    def not_ok(cls: type[_TestAnything], *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> type[_TestAnything]: ...
    @classmethod
    def comment(cls: type[_TestAnything], *message: str) -> type[_TestAnything]: ...
    @classmethod
    def diagnostic(cls: type[_TestAnything], *message: str, **kwargs: str | tuple[str, ...]) -> None: ...
    @classmethod
    def subtest(cls: type[_TestAnything], name: str | None = None) -> ContextManager[type[_TestAnything]]: ...
    @staticmethod
    def bail_out(*message: str) -> NoReturn: ...
    @classmethod
    def end(cls: type[_TestAnything], skip_reason: str = '') -> type[_TestAnything]: ...
    @classmethod
    def suppress(cls: type[_TestAnything]) -> ContextManager[type[_TestAnything]]: ...
    @classmethod
    def strict(cls: type[_TestAnything]) -> ContextManager[type[_TestAnything]]: ...
    @classmethod
    def _skip_count(cls: type[_TestAnything]) -> int: ...
    @classmethod
    def _test_point_count(cls: type[_TestAnything]) -> int: ...
    @classmethod
    def _diagnostic(
        cls: type[_TestAnything], *message: str, **kwargs: str | tuple[str, ...]
    ) -> None: ...

def _warn_format(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""

def _warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: TextIO | None = None,
) -> None:
    """Emit a TAP formatted warning, does not introspect."""