"""Base types and protocols for TAP-Producer."""

from __future__ import annotations

import sys
import warnings
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING
from typing import Callable
from typing import ClassVar
from typing import ContextManager
from typing import Counter
from typing import NoReturn
from typing import Protocol
from typing import TextIO
from typing import runtime_checkable

if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

FormatWarningType = Callable[[Warning | str, type[Warning], str, int, str | None], str]
ShowWarningType = Callable[
    [Warning | str, type[Warning], str, int, TextIO | None, str | None], None
]


@runtime_checkable
class _LockType(AbstractContextManager[bool], Protocol):
    """Static lock type."""

    def acquire(  # noqa: DC102
        self: _LockType, blocking: bool = ..., timeout: float = ...
    ) -> bool: ...
    def release(self: _LockType) -> None: ...  # noqa: DC102


@runtime_checkable
class _TestAnything(AbstractContextManager['_TestAnything'], Protocol):
    """Static type for the TAP-Producer context decorator."""

    _formatwarning: ClassVar[FormatWarningType]
    _showwarning: ClassVar[ShowWarningType]
    _count: ClassVar[Counter[str]]
    _version: ClassVar[int]
    __lock: ClassVar[_LockType]
    __plan: int | None
    __version: int | None

    def __init__(  # noqa: DC104
        self: _TestAnything, plan: int | None = None, version: int | None = None
    ) -> None: ...

    def __enter__(self: _TestAnything) -> _TestAnything:  # noqa: DC104
        ...

    def __exit__(  # noqa: DC104
        self: _TestAnything,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...

    @classmethod
    def version(  # noqa: DC102
        cls: type[_TestAnything], version: int = ...
    ) -> _TestAnything: ...

    @classmethod
    def plan(  # noqa: DC102
        cls: type[_TestAnything],
        count: int | None = None,
        skip_reason: str = '',
        skip_count: int | None = None,
    ) -> _TestAnything: ...

    @classmethod
    def ok(  # noqa: DC102
        cls: type[_TestAnything],
        *message: str,
        skip: bool = False,
        **diagnostic: str | tuple[str, ...],
    ) -> _TestAnything: ...

    @classmethod
    def not_ok(  # noqa: DC102
        cls: type[_TestAnything],
        *message: str,
        skip: bool = False,
        **diagnostic: str | tuple[str, ...],
    ) -> _TestAnything: ...

    @classmethod
    def comment(  # noqa: DC102
        cls: type[_TestAnything], *message: str
    ) -> type[_TestAnything]: ...

    @classmethod
    def diagnostic(  # noqa: DC102
        cls: type[_TestAnything], *message: str, **kwargs: str | tuple[str, ...]
    ) -> None: ...

    @classmethod
    def subtest(  # noqa: DC102
        cls: type[_TestAnything], name: str | None = None
    ) -> ContextManager[_TestAnything]: ...

    @staticmethod
    def bail_out(*message: str) -> NoReturn: ...  # noqa: DC102

    @classmethod
    def end(  # noqa: DC102
        cls: type[_TestAnything], skip_reason: str = ''
    ) -> _TestAnything: ...

    @classmethod
    def suppress(  # noqa: DC102
        cls: type[_TestAnything],
    ) -> ContextManager[_TestAnything]: ...

    @classmethod
    def strict(cls: type[_TestAnything]) -> ContextManager[_TestAnything]: ...  # noqa: DC102

    @classmethod
    def _skip_count(cls: type[_TestAnything]) -> int: ...  # noqa: DC103

    @classmethod
    def _test_point_count(cls: type[_TestAnything]) -> int: ...  # noqa: DC103

    @classmethod
    def _diagnostic(  # noqa: DC103
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
    return f'{message}{category.__name__}\n'  # pragma: no cover


def _warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: TextIO | None = None,
) -> None:
    """Emit a TAP formatted warning, does not introspect."""
    sys.stderr.write(  # pragma: no cover
        warnings.formatwarning(message, category, filename, lineno),
    )
