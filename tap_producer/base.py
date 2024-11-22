"""Base types and protocols for TAP-Producer."""

from __future__ import annotations

import os
import sys
import warnings
from contextlib import AbstractContextManager
from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
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
    from collections.abc import Iterator
    from types import TracebackType

FormatWarningType = Callable[[Warning | str, type[Warning], str, int, str | None], str]
ShowWarningType = Callable[
    [Warning | str, type[Warning], str, int, TextIO | None, str | None], None
]

OK = 'ok'
NOT_OK = 'not_ok'
SKIP = 'skip'
PLAN = 'plan'
VERSION = 'version'
SUBTEST = 'subtest_level'
INDENT = '    '
DEFAULT_TAP_VERSION = 12


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
    _lock: ClassVar[_LockType]
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


@contextmanager
def suppress_wrapper(
    cls: type[_TestAnything],
) -> Iterator[type[_TestAnything]]:  # pragma: defer to E2E
    """workaround for pyright"""
    warnings.simplefilter('ignore')
    null = Path(os.devnull).open('w')
    try:
        with redirect_stdout(null):
            with redirect_stderr(null):
                yield cls
    finally:
        null.close()
        warnings.resetwarnings()


@contextmanager
def subtest_wrapper(
    cls: type[_TestAnything], name: str | None = None
) -> Iterator[type[_TestAnything]]:
    """workaround for pyright"""
    if cls._version == DEFAULT_TAP_VERSION:
        warnings.warn(
            'called subtest but TAP version is set to 12',
            category=RuntimeWarning,
            stacklevel=2,
        )
    cls.comment(f'Subtest: {name}' if name else 'Subtest')
    with cls._lock:
        parent_count = cls._count.copy()
        cls._count = Counter(
            ok=0,
            not_ok=0,
            skip=0,
            plan=0,
            version=1,
            subtest_level=parent_count[SUBTEST] + 1,
        )
    try:
        yield cls
    finally:
        if cls._count[PLAN] < 1:
            cls.plan(cls._test_point_count())

        if cls._count[OK] > 0 and cls._count[SKIP] < 1 and cls._count[NOT_OK] < 1:
            with cls._lock:
                cls._count = parent_count
            cls.ok(name if name else 'Subtest')
        elif cls._count[NOT_OK] > 0:  # pragma: no cover
            with cls._lock:
                cls._count = parent_count
            cls.not_ok(name if name else 'Subtest')


@contextmanager
def strict_wrapper(
    cls: type[_TestAnything],
) -> Iterator[type[_TestAnything]]:  # pragma: defer to E2E
    """workaround for pyright"""
    warnings.simplefilter('error', category=RuntimeWarning, append=True)
    try:
        yield cls
    finally:
        warnings.resetwarnings()


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
    file: str | None = None,
) -> None:
    """Emit a TAP formatted warning, does not introspect."""
    sys.stderr.write(  # pragma: no cover
        warnings.formatwarning(message, category, filename, lineno),
    )
