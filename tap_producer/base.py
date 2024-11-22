"""Base types and protocols for TAP-Producer."""

from __future__ import annotations

import os
import sys
import warnings
from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Counter
from typing import TextIO

if TYPE_CHECKING:
    from collections.abc import Iterator

    from tap_producer.protocol import _TestAnything

OK = 'ok'
NOT_OK = 'not_ok'
SKIP = 'skip'
PLAN = 'plan'
VERSION = 'version'
SUBTEST = 'subtest_level'
INDENT = '    '
DEFAULT_TAP_VERSION = 12


def validate_version_args(cls: type[_TestAnything], version: int) -> int | None:
    """Warn if ``TAP.version`` is not called with valid arguments."""
    if cls._count[VERSION] > 0 and cls._count.total() > 0:
        warnings.warn(
            'TAP.version called during a session must be called first',
            RuntimeWarning,
            stacklevel=2,
        )
        return None  # pragma: no cover
    if version > 14 or version < 12:
        with cls._lock:
            version = DEFAULT_TAP_VERSION
        warnings.warn(
            f'Invalid TAP version: {version}, using 12',
            category=RuntimeWarning,
            stacklevel=2,
        )
    return version


def validate_plan_args(
    cls: type[_TestAnything], count: int | None, skip_count: int | None, skip_reason: str
) -> tuple[int, int]:
    """Warn if ``TAP.plan`` is not called with valid arguments."""
    count = cls._test_point_count() if count is None else count
    skip_count = cls._skip_count() if skip_count is None else skip_count
    if skip_reason != '' and skip_count == 0:
        warnings.warn(  # pragma: no cover
            'unnecessary argument "skip_reason" to TAP.plan',
            RuntimeWarning,
            stacklevel=2,
        )
    if cls._count[PLAN] > 0:
        warnings.warn(
            'TAP.plan called more than once during session.',
            RuntimeWarning,
            stacklevel=2,
        )
    return count, skip_count


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


def begin_subtest(cls: type[_TestAnything], name: str | None) -> Counter[str]:
    """Start (optionally) named subtest, return original test counter."""
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
    return parent_count


def end_subtest(cls: type[_TestAnything], parent_count: Counter[str], message: str) -> None:
    """End a subtest and restore counter."""
    if cls._count[PLAN] < 1:
        cls.plan(cls._test_point_count())

    if cls._count[OK] > 0 and cls._count[SKIP] < 1 and cls._count[NOT_OK] < 1:
        with cls._lock:
            cls._count = parent_count
        cls.ok(message)
    elif cls._count[NOT_OK] > 0:  # pragma: no cover
        with cls._lock:
            cls._count = parent_count
        cls.not_ok(message)


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
    parent_count = begin_subtest(cls, name)
    try:
        yield cls
    finally:
        end_subtest(cls, parent_count, name if name else 'Subtest')


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
