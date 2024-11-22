# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
"""Test Anything Protocol tools."""
from __future__ import annotations

import sys
import warnings
from collections import Counter
from contextlib import ContextDecorator
from threading import Lock
from typing import TYPE_CHECKING
from typing import ContextManager
from typing import NoReturn

import yaml

from tap_producer.base import DEFAULT_TAP_VERSION
from tap_producer.base import INDENT
from tap_producer.base import NOT_OK
from tap_producer.base import OK
from tap_producer.base import PLAN
from tap_producer.base import SKIP
from tap_producer.base import SUBTEST
from tap_producer.base import VERSION
from tap_producer.base import _TestAnything
from tap_producer.base import _warn
from tap_producer.base import _warn_format
from tap_producer.base import strict_wrapper
from tap_producer.base import subtest_wrapper
from tap_producer.base import suppress_wrapper

if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

__all__ = ('TAP', 'DEFAULT_TAP_VERSION', '_TestAnything')


class TAP(_TestAnything, ContextDecorator):
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
    _lock = __lock

    def __init__(
        self: _TestAnything,
        plan: int | None = None,
        version: int | None = None,
    ) -> None:
        """Initialize a TAP decorator.

        :param plan: number of test points planned, defaults to None
        :type plan: int | None, optional
        :param version: the version of TAP to set, defaults to None
        :type version: int | None, optional
        """
        self.__plan = plan
        self.__version = version

    def __enter__(self: _TestAnything) -> _TestAnything:
        """TAP context decorator entry.

        :return: a context decorator
        :rtype: TAP
        """
        if self.__version is not None:
            type(self).version(self.__version)
        if self.__plan is not None:
            type(self).plan(self.__plan)
        return self

    def __exit__(
        self: _TestAnything,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Exit the TAP context and propagate exceptions."""
        with type(self).__lock:
            skip_count = type(self)._count[SKIP]
        type(self).end(skip_reason=str(exc_value) if exc_value and skip_count > 0 else '')
        return False

    @classmethod
    def version(
        cls: type[_TestAnything], version: int = DEFAULT_TAP_VERSION
    ) -> type[_TestAnything]:
        """Set the TAP version to use, must be called first.

        :param version: _description_, defaults to 12
        :type version: int, optional
        :return: a context decorator
        :rtype: TAP
        """
        if cls._count[VERSION] < 1 and cls._count.total() < 1:
            with cls.__lock:
                cls._count[VERSION] += 1
                cls._version = version
            if cls._version > 14 or cls._version < 12:
                with cls.__lock:
                    cls._version = DEFAULT_TAP_VERSION
                warnings.warn(
                    f'Invalid TAP version: {cls._version}, using 12',
                    category=RuntimeWarning,
                    stacklevel=2,
                )
                return cls  # pragma: no cover
            elif cls._version == DEFAULT_TAP_VERSION:
                return cls
            sys.stdout.write(f'TAP version {cls._version}\n')
        else:
            warnings.warn(
                'TAP.version called during a session must be called first',
                RuntimeWarning,
                stacklevel=2,
            )
        return cls

    @classmethod
    def plan(
        cls: type[_TestAnything],
        count: int | None = None,
        skip_reason: str = '',
        skip_count: int | None = None,
    ) -> type[_TestAnything]:
        """Print a TAP test plan.

        :param count: planned test count, defaults to None
        :type count: int | None, optional
        :param skip_reason: diagnostic to print, defaults to ''
        :type skip_reason: str, optional
        :param skip_count: number of tests skipped, defaults to None
        :type skip_count: int | None, optional
        :return: a context decorator
        :rtype: TAP
        """
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
        with cls.__lock:
            cls._count[PLAN] += 1
        directive = f' # SKIP {skip_reason}' if skip_reason != '' else ''
        if skip_count > 0:
            cls.comment('items skipped', str(skip_count))
        sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}1..{count}{directive}\n')
        return cls

    @classmethod
    def ok(
        cls: type[_TestAnything],
        *message: str,
        skip: bool = False,
        **diagnostic: str | tuple[str, ...],
    ) -> type[_TestAnything]:
        r"""Mark a test result as successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        :param \*\*diagnostic: to be presented as YAML in TAP version > 13
        :type \*\*diagnostic: str | tuple[str, ...]
        :return: a context decorator
        :rtype: TAP
        """
        with cls.__lock:
            cls._count[OK] += 1
            cls._count[SKIP] += 1 if skip else 0
        directive = '' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip().replace('#', r'\#')
        description = f'- {formatted}' if len(formatted) > 0 else ''
        indent = INDENT * cls._count[SUBTEST]
        sys.stdout.write(
            f'{indent}ok {cls._test_point_count()} {description} {directive}\n',
        )
        if diagnostic:
            cls._diagnostic(**diagnostic)
        return cls

    @classmethod
    def not_ok(
        cls: type[_TestAnything],
        *message: str,
        skip: bool = False,
        **diagnostic: str | tuple[str, ...],
    ) -> type[_TestAnything]:
        r"""Mark a test result as :strong:`not` successful.

        .. versionchanged:: 1.5
           Calling with ``skip=True`` no longer emits a Python warning.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        :param \*\*diagnostic: to be presented as YAML in TAP version > 13
        :type \*\*diagnostic: str | tuple[str, ...]
        :return: a context decorator
        :rtype: TAP
        """
        indent = INDENT * cls._count[SUBTEST]
        with cls.__lock:
            cls._count[NOT_OK] += 1
            cls._count[SKIP] += 1 if skip else 0
            if not skip:
                warnings.formatwarning = _warn_format
                warnings.showwarning = _warn  # type: ignore
        directive = '' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip().replace('#', r'\#')
        description = f'- {formatted}' if len(formatted) > 0 else ''
        sys.stdout.write(
            f'{indent}not ok {cls._test_point_count()} {description} {directive}\n',
        )
        if diagnostic:
            cls._diagnostic(**diagnostic)
        if not skip:
            warnings.warn(
                f'{indent}# {cls._test_point_count()} {formatted} {directive}',
                RuntimeWarning,
                stacklevel=2,
            )
            with cls.__lock:  # pragma: no cover
                warnings.formatwarning = cls._formatwarning  # pragma: no cover
                warnings.showwarning = cls._showwarning  # pragma: no cover
        return cls

    @classmethod
    def comment(cls: type[_TestAnything], *message: str) -> type[_TestAnything]:
        r"""Print a message to the TAP stream.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :return: a context decorator
        :rtype: TAP
        """
        formatted = ' - '.join(message).strip()
        sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}# {formatted}\n')
        return cls

    @classmethod
    def diagnostic(
        cls: type[_TestAnything], *message: str, **kwargs: str | tuple[str, ...]
    ) -> None:
        r"""Print a diagnostic message.

        .. deprecated:: 1.2
           Use the \*\*diagnostic kwargs to TAP.ok and TAP.not_ok instead.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param \*\*kwargs: diagnostics to be presented as YAML in TAP version > 13
        :type \*\*kwargs: str | tuple[str, ...]
        """
        warnings.warn(
            'Calling TAP.diagnostic is deprecated and will be removed in a later version.',
            RuntimeWarning,
            stacklevel=2,
        )
        cls._diagnostic(*message, **kwargs)

    @classmethod
    def _diagnostic(
        cls: type[_TestAnything], *message: str, **kwargs: str | tuple[str, ...]
    ) -> None:
        r"""Print a diagnostic message.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param \*\*kwargs: diagnostics to be presented as YAML in TAP version > 13
        :type \*\*kwargs: str | tuple[str, ...]
        """
        if cls._version == DEFAULT_TAP_VERSION:
            message += tuple(f'{k}: {v}' for k, v in kwargs.items())
            formatted = ' - '.join(message).strip()
            sys.stdout.write(f'{INDENT * cls._count[SUBTEST]}# {formatted}\n')
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
    def subtest(
        cls: type[_TestAnything], name: str | None = None
    ) -> ContextManager[type[_TestAnything]]:
        """Start a TAP subtest document, name is optional.
        :return: a context manager
        :rtype: ContextManager[TAP]
        """
        return subtest_wrapper(cls, name=name)

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        r"""Print a bail out message and exit.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """
        print('Bail out!', *message, file=sys.stdout)
        sys.exit(1)

    @classmethod
    def end(cls: type[_TestAnything], skip_reason: str = '') -> type[_TestAnything]:
        """End a TAP diagnostic and reset the counters.

        .. versionchanged:: 1.1
           No longer exits, just resets the counts.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        :return: a context decorator
        :rtype: TAP
        """
        skip_count = cls._skip_count()
        if skip_reason != '' and skip_count == 0:
            warnings.warn(
                'unnecessary argument "skip_reason" to TAP.end',
                RuntimeWarning,
                stacklevel=2,
            )
        if cls._count[PLAN] < 1:
            cls.plan(count=None, skip_reason=skip_reason, skip_count=skip_count)
        cls._count = Counter(ok=0, not_ok=0, skip=0, plan=0, version=0, subtest_level=0)
        return cls

    @classmethod
    def suppress(
        cls: type[_TestAnything],
    ) -> ContextManager[type[_TestAnything]]:  # pragma: defer to python
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.

        :return: a context manager
        :rtype: ContextManager[TAP]
        """
        return suppress_wrapper(cls)

    @classmethod
    def strict(
        cls: type[_TestAnything],
    ) -> ContextManager[type[_TestAnything]]:  # pragma: defer to OZI
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        :return: a context manager
        :rtype: ContextManager[TAP]
        """

        return strict_wrapper(cls)

    @classmethod
    def _skip_count(
        cls: type[_TestAnything],
    ) -> int:
        """Pop the current skip count.

        :return: skip count
        :rtype: int
        """
        with cls.__lock:
            return cls._count.pop(SKIP, 0)

    @classmethod
    def _test_point_count(cls: type[_TestAnything]) -> int:
        """Get the proper count of ok, not ok, and skipped."""
        with cls.__lock:
            return (
                cls._count.total()
                - cls._count[SUBTEST]
                - cls._count[VERSION]
                - cls._count[PLAN]
            ) - cls._count[SKIP]
