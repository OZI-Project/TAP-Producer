from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TextIO

from tap_producer.protocol import _TestAnything

DEFAULT_TAP_VERSION: int
OK: str
NOT_OK: str
SKIP: str
PLAN: str
VERSION: str
SUBTEST: str
INDENT: str

def validate_version_args(cls: type[_TestAnything], version: int) -> int | None:
    """Warn if ``TAP.version`` is not called with valid arguments."""

def validate_plan_args(
    cls: type[_TestAnything],
    count: int | None,
    skip_count: int | None,
    skip_reason: str
) -> tuple[int, int]:
    """Warn if ``TAP.plan`` is not called with valid arguments."""

@contextmanager
def suppress_wrapper(cls: type[_TestAnything]) -> Iterator[type[_TestAnything]]:
    """workaround for pyright"""

@contextmanager
def subtest_wrapper(
    cls: type[_TestAnything], name: str | None = None
) -> Iterator[type[_TestAnything]]:
    """workaround for pyright"""

@contextmanager
def strict_wrapper(cls: type[_TestAnything]) -> Iterator[type[_TestAnything]]:
    """workaround for pyright"""

def begin_subtest(cls: type[_TestAnything], name: str | None) -> Counter[str]:
    """Start (optionally) named subtest, return original test counter."""

def end_subtest(cls: type[_TestAnything], parent_count: Counter[str], message: str) -> None:
    """End a subtest and restore counter."""

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
    file: str | None = None,
) -> None:
    """Emit a TAP formatted warning, does not introspect."""