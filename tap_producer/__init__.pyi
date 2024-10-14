"""Test Anything Protocol tools."""

from contextlib import ContextDecorator
from contextlib import contextmanager
from typing import Any
from typing import Generator
from typing import Literal
from typing import NoReturn

DEFAULT_TAP_VERSION = 12

__all__ = ('TAP', 'DEFAULT_TAP_VERSION')

class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Not known to be thread-safe.

    .. versionchanged:: 0.1.5
        Added a __lock to counter calls. However, use in a threaded environment untested.
    """
    _formatwarning = ...
    _showwarning = ...
    _count = ...
    _version = ...
    __lock = ...

    def __init__(self: TAP, plan: int | None = None, version: int | None = None) -> None:
        ...

    def __enter__(self) -> TAP:
        ...
    
    def __exit__(self, exc) -> Literal[False]:
        ...

    @classmethod
    def version(cls, version: int = ...) -> None:
        """Set the TAP version to use, defaults to 12, must be called first."""

    @classmethod
    def end(cls, skip_reason: str = ...) -> NoReturn:
        """End a TAP diagnostic and reset the counters.

        .. versionchanged:: 1.1
           No longer exits, just resets the counts.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        """

    @classmethod
    def comment(cls, *message: str) -> None:
        r"""Print a message to the TAP stream.

        .. note::

           If using TAP version < 14, prints a diagnostic.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """

    @staticmethod
    def diagnostic(*message: str, **kwargs: str | tuple[str, ...]) -> None:
        r"""Print a diagnostic message.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param \*\*kwargs: diagnostics to be presented as YAML in TAP version > 13
        :type \*\*kwargs: str | tuple[str, ...]
        """

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        r"""Print a bail out message and exit.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """

    @classmethod
    def plan(
        cls,
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

    @classmethod
    @contextmanager
    def subtest(cls, name: str | None = None) -> Generator[None, Any, None]:
        """Start a TAP subtest document, name is optional."""

    @staticmethod
    @contextmanager
    def suppress() -> Generator[None, Any, None]:
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.
        """

    @staticmethod
    @contextmanager
    def strict() -> Generator[None, Any, None]:
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        """

    @classmethod
    def ok(cls, *message: str, skip: bool = ...) -> None:
        r"""Mark a test result as successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """

    @classmethod
    def not_ok(cls, *message: str, skip: bool = ...) -> None:
        r"""Mark a test result as :strong:`not` successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """
   
    @classmethod
    def _skip_count(
        cls: type[TAP],
    ) -> int:
        """Pop the current skip count.

        :return: skip count
        :rtype: int
        """
        ...

    @classmethod
    def _test_point_count(cls: type[TAP]) -> int:
        """Get the proper count of ok, not ok, and skipped."""
        ...