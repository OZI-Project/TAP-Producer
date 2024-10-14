# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
"""Test Anything Protocol tools."""
from __future__ import annotations

import os
import sys
import warnings
from collections import Counter
from contextlib import ContextDecorator
from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING
from typing import Generator
from typing import Literal
from typing import NoReturn
from typing import TextIO

import yaml

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

OK = 'ok'
NOT_OK = 'not_ok'
SKIP = 'skip'
PLAN = 'plan'
VERSION = 'version'
SUBTEST = 'subtest_level'
INDENT = '    '
DEFAULT_TAP_VERSION = 12

__all__ = ('TAP', 'DEFAULT_TAP_VERSION')


def _warn_format(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'{message} - {category.__name__}\n'  # pragma: no cover


def _warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: TextIO | None = None,
    stacklevel: int = 1,
) -> None:
    """emit a TAP formatted warning."""
    sys.stderr.write(  # pragma: no cover
        warnings.formatwarning(message, category, filename, lineno),
    )


class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Not known to be thread-safe.

    .. versionchanged:: 0.1.5
        Added a __lock to counter calls. However, use in a threaded environment untested.
    """

    _formatwarning = staticmethod(warnings.formatwarning)
    _showwarning = staticmethod(warnings.showwarning)
    _count = Counter(ok=0, not_ok=0, skip=0, plan=0, version=0, subtest_level=0)
    _version = DEFAULT_TAP_VERSION
    __lock = Lock()

    def __init__(self: TAP, plan: int | None = None, version: int | None = None) -> None:
        self.__plan = plan
        self.__version = version

    def __enter__(self: Self) -> Self:
        if self.__version:
            type(self).version(self.__version)
        if self.__plan:
            type(self).plan(self.__plan)
        return self

    def __exit__(self: Self, *exc: object) -> Literal[False]:
        return False

    @classmethod
    def version(cls: type[Self], version: int = DEFAULT_TAP_VERSION) -> None:
        """Set the TAP version to use, defaults to 12, must be called first."""
        if cls._count[VERSION] < 1 and cls._count.total() < 1:
            with cls.__lock:
                cls._count[VERSION] += 1
                cls._version = version
            if cls._version > 14 or cls._version < 12:
                with cls.__lock:
                    cls._version = DEFAULT_TAP_VERSION
                cls.diagnostic(f'Invalid TAP version: {cls._version}, using 12')
                return
            elif cls._version == DEFAULT_TAP_VERSION:
                return
            sys.stdout.write(f'TAP version {cls._version}\n')
        else:
            cls.diagnostic(
                'TAP.version called during a session',
                'must be called first',
                f'TAP version {cls._version}',
            )

    @classmethod
    def plan(  # noqa: C901
        cls: type[Self],
        count: int | None = None,
        skip_reason: str = '',
        skip_count: int | None = None,
    ) -> None:
        """Print a TAP test plan.

        :param count: planned test count, defaults to None
        :type count: int | None, optional
        :param skip_reason: diagnostic to print, defaults to ''
        :type skip_reason: str, optional
        :param skip_count: number of tests skipped, defaults to None
        :type skip_count: int | None, optional
        """
        count = cls._test_point_count() if count is None else count
        if skip_count is None:
            skip_count = cls._skip_count()
        if skip_reason != '' and skip_count == 0:
            cls.diagnostic('unnecessary argument "skip_reason" to TAP.plan')
        if cls._count[PLAN] < 1:
            with cls.__lock:
                cls._count[PLAN] += 1
            match [count, skip_reason, skip_count]:
                case [n, r, s] if r == '' and s > 0:  # type: ignore
                    cls.diagnostic('items skipped', str(s))
                    sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}1..{n}\n')
                case [n, r, s] if r != '' and s > 0:  # type: ignore
                    cls.diagnostic('items skipped', str(s))
                    sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}1..{n} # SKIP {r}\n')
                case [n, r, s] if r == '' and s == 0:
                    sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}1..{n}\n')
                case _:  # pragma: no cover
                    cls.bail_out('TAP.plan failed due to invalid arguments.')
        else:
            cls.diagnostic('TAP.plan called more than once during session.')

    @classmethod
    def ok(cls: type[Self], *message: str, skip: bool = False) -> None:
        r"""Mark a test result as successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """
        with cls.__lock:
            cls._count[OK] += 1
            cls._count[SKIP] += 1 if skip else 0
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip().replace('#', r'\#')
        indent = INDENT * cls._count[SUBTEST]
        sys.stdout.write(
            f'{indent}ok {cls._test_point_count()} {directive} {formatted}\n',
        )

    @classmethod
    def not_ok(cls: type[Self], *message: str, skip: bool = False) -> None:
        r"""Mark a test result as :strong:`not` successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """
        indent = INDENT * cls._count[SUBTEST]
        with cls.__lock:
            cls._count[NOT_OK] += 1
            cls._count[SKIP] += 1 if skip else 0
            warnings.formatwarning = _warn_format
            warnings.showwarning = _warn  # type: ignore
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip().replace('#', r'\#')
        sys.stdout.write(
            f'{indent}not ok {cls._test_point_count()} {directive} {formatted}\n',
        )
        warnings.warn(
            f'{indent}# {cls._test_point_count()} {directive} {formatted}',
            RuntimeWarning,
            stacklevel=2,
        )
        with cls.__lock:  # pragma: no cover
            warnings.formatwarning = cls._formatwarning  # pragma: no cover
            warnings.showwarning = cls._showwarning  # pragma: no cover

    @classmethod
    def comment(cls: type[Self], *message: str) -> None:
        r"""Print a message to the TAP stream.

        .. note::

           If using TAP version < 14, prints a diagnostic.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """
        if cls._version == 14:
            formatted = ' - '.join(message).strip()
            sys.stderr.write(f'{INDENT * cls._count[SUBTEST]}# {formatted}\n')
        else:
            cls.diagnostic(*message)

    @classmethod
    def diagnostic(cls: type[Self], *message: str, **kwargs: str | tuple[str, ...]) -> None:
        r"""Print a diagnostic message.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param \*\*kwargs: diagnostics to be presented as YAML in TAP version > 13
        :type \*\*kwargs: str | tuple[str, ...]
        """
        if cls._version == DEFAULT_TAP_VERSION:
            message += tuple(f'{k}: {v}' for k, v in kwargs.items())
            formatted = ' - '.join(message).strip()
            sys.stderr.write(f'{INDENT * cls._count[SUBTEST]}# {formatted}\n')
        else:
            kwargs |= {'message': ' - '.join(message).strip()} if len(message) > 0 else {}
            for i in yaml.dump(
                kwargs,
                indent=2,
                explicit_start=True,
                explicit_end=True,
                sort_keys=False,
            ).split('\n'):
                sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}  {i}\n')

    @classmethod
    @contextmanager
    def subtest(cls: type[Self], name: str | None = None) -> Generator[None, Any, None]:
        """Start a TAP subtest document, name is optional."""
        comment = f'Subtest: {name}' if name else 'Subtest'
        cls.diagnostic(comment)
        with cls.__lock:
            parent_count = cls._count.copy()
            cls._count = Counter(
                ok=0,
                not_ok=0,
                skip=0,
                plan=0,
                version=1,
                subtest_level=parent_count[SUBTEST] + 1,
            )
        yield
        if cls._count[PLAN] < 1:
            cls.plan(cls._test_point_count())

        if cls._count[OK] > 0 and cls._count[SKIP] < 1 and cls._count[NOT_OK] < 1:
            with cls.__lock:
                cls._count = parent_count
            cls.ok(name if name else 'Subtest')
        elif cls._count[NOT_OK] > 0:  # pragma: no cover
            with cls.__lock:
                cls._count = parent_count
            cls.not_ok(name if name else 'Subtest')

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        r"""Print a bail out message and exit.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """
        print('Bail out!', *message, file=sys.stderr)
        sys.exit(1)

    @classmethod
    def end(cls: type[Self], skip_reason: str = '') -> None:
        """End a TAP diagnostic and reset the counters.

        .. versionchanged:: 1.1
           No longer exits, just resets the counts.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        """
        skip_count = cls._skip_count()
        if skip_reason != '' and skip_count == 0:
            cls.diagnostic('unnecessary argument "skip_reason" to TAP.end')
        if cls._count[PLAN] < 1:
            cls.plan(count=None, skip_reason=skip_reason, skip_count=skip_count)
        cls._count = Counter(ok=0, not_ok=0, skip=0, plan=0, version=0, subtest_level=0)

    @staticmethod
    @contextmanager
    def suppress() -> Generator[None, Any, None]:  # pragma: defer to python
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.
        """
        warnings.simplefilter('ignore')
        null = Path(os.devnull).open('w')
        with redirect_stdout(null):
            with redirect_stderr(null):
                yield
        null.close()
        warnings.resetwarnings()

    @staticmethod
    @contextmanager
    def strict() -> Generator[None, Any, None]:  # pragma: defer to OZI
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        """
        warnings.simplefilter('error', category=RuntimeWarning, append=True)
        yield
        warnings.resetwarnings()

    @classmethod
    def _skip_count(
        cls: type[Self],
    ) -> int:
        """Pop the current skip count.

        :return: skip count
        :rtype: int
        """
        with cls.__lock:
            return cls._count.pop(SKIP, 0)

    @classmethod
    def _test_point_count(cls: type[Self]) -> int:
        """Get the proper count of ok, not ok, and skipped."""
        with cls.__lock:
            return (
                cls._count.total()
                - cls._count[SUBTEST]
                - cls._count[VERSION]
                - cls._count[PLAN]
            ) - cls._count[SKIP]
