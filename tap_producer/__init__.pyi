from contextlib import ContextDecorator
from types import TracebackType
from typing import ClassVar
from typing import ContextManager
from typing import Counter
from typing import NoReturn

from tap_producer.base import DEFAULT_TAP_VERSION
from tap_producer.protocol import FormatWarningType
from tap_producer.protocol import ShowWarningType
from tap_producer.protocol import _LockType
from tap_producer.protocol import _TestAnything

__all__ = ('TAP', 'DEFAULT_TAP_VERSION', '_TestAnything')
DEFAULT_TAP_VERSION = DEFAULT_TAP_VERSION

class TAP(_TestAnything, ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Not known to be thread-safe.

    .. versionchanged:: 0.1.5
        Added a __lock to counter calls. However, use in a threaded environment untested.
    """
    _formatwarning: ClassVar[FormatWarningType]
    _showwarning: ClassVar[ShowWarningType]
    _count: ClassVar[Counter[str]]
    _version: ClassVar[int]
    __lock: ClassVar[_LockType]
    _lock: ClassVar[_LockType]
    __plan: int | None
    __version: int | None

    def __init__(self, plan: int | None = None, version: int | None = None) -> None:
        """Initialize a TAP decorator.

        :param plan: number of test points planned, defaults to None
        :type plan: int | None, optional
        :param version: the version of TAP to set, defaults to None
        :type version: int | None, optional
        """
    def __enter__(self) -> _TestAnything:
        """TAP context decorator entry.

        :return: a context decorator
        :rtype: TAP
        """
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None:
        """Exit the TAP context and propagate exceptions."""
    @classmethod
    def version(cls, version: int = ...) -> type[_TestAnything]:
        """Set the TAP version to use, must be called first.

        :param version: _description_, defaults to 12
        :type version: int, optional
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def plan(cls, count: int | None = None, skip_reason: str = '', skip_count: int | None = None) -> type[_TestAnything]:
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
    @classmethod
    def ok(cls, *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> type[_TestAnything]:
        """Mark a test result as successful.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        :param \\*\\*diagnostic: to be presented as YAML in TAP version > 13
        :type \\*\\*diagnostic: str | tuple[str, ...]
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def not_ok(cls, *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> type[_TestAnything]:
        """Mark a test result as :strong:`not` successful.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        :param \\*\\*diagnostic: to be presented as YAML in TAP version > 13
        :type \\*\\*diagnostic: str | tuple[str, ...]
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def comment(cls, *message: str) -> type[_TestAnything]:
        """Print a message to the TAP stream.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def diagnostic(cls, *message: str, **kwargs: str | tuple[str, ...]) -> None:
        """Print a diagnostic message.

        .. deprecated:: 1.2
           Use the \\*\\*diagnostic kwargs to TAP.ok and TAP.not_ok instead.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        :param \\*\\*kwargs: diagnostics to be presented as YAML in TAP version > 13
        :type \\*\\*kwargs: str | tuple[str, ...]
        """
    @classmethod
    def subtest(cls, name: str | None = None) -> ContextManager[type[_TestAnything]]:
        """Start a TAP subtest document, name is optional.
        :return: a context manager
        :rtype: ContextManager[TestAnything]
        """
    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        """Print a bail out message and exit.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        """
    @classmethod
    def end(cls, skip_reason: str = '') -> type[_TestAnything]:
        """End a TAP diagnostic and reset the counters.

        .. versionchanged:: 1.1
           No longer exits, just resets the counts.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def suppress(cls) -> ContextManager[type[_TestAnything]]:
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.

        :return: a context manager
        :rtype: ContextManager[TestAnything]
        """
    @classmethod
    def strict(cls) -> ContextManager[type[_TestAnything]]:
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        :return: a context manager
        :rtype: ContextManager[TestAnything]
        """
