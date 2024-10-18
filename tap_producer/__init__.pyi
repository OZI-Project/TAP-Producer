from contextlib import ContextDecorator
from typing import ContextManager
from typing import Generator
from typing import Literal
from typing import NoReturn

__all__ = ['TAP', 'DEFAULT_TAP_VERSION']

DEFAULT_TAP_VERSION: int

class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Not known to be thread-safe.

    .. versionchanged:: 0.1.5
        Added a __lock to counter calls. However, use in a threaded environment untested.
    """
    def __init__(self, plan: int | None = None, version: int | None = None) -> None:
        """Initialize a TAP decorator.

        :param plan: number of test points planned, defaults to None
        :type plan: int | None, optional
        :param version: the version of TAP to set, defaults to None
        :type version: int | None, optional
        """
    def __enter__(self) -> TAP:
        """TAP context decorator entry.

        :return: a context decorator
        :rtype: TAP
        """
    def __exit__(self, *exc: Exception) -> Literal[False]:
        """Exit the TAP context and propagate exceptions."""
    @classmethod
    def version(cls, version: int = ...) -> TAP:
        """Set the TAP version to use, must be called first.

        :param version: _description_, defaults to 12
        :type version: int, optional
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def plan(cls, count: int | None = None, skip_reason: str = '', skip_count: int | None = None) -> TAP:
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
    def ok(cls, *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> TAP:
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
    def not_ok(cls, *message: str, skip: bool = False, **diagnostic: str | tuple[str, ...]) -> TAP:
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
    def comment(cls, *message: str) -> TAP:
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
    def subtest(cls, name: str | None = None) -> ContextManager[TAP]:
        """Start a TAP subtest document, name is optional.
        :return: a context generator
        :rtype: Generator[TAP]
        """
    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        """Print a bail out message and exit.

        :param \\*message: messages to print to TAP output
        :type \\*message: tuple[str]
        """
    @classmethod
    def end(cls, skip_reason: str = '') -> TAP:
        """End a TAP diagnostic and reset the counters.

        .. versionchanged:: 1.1
           No longer exits, just resets the counts.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def suppress(cls) -> ContextManager[TAP]:
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.

        :return: a context decorator
        :rtype: TAP
        """
    @classmethod
    def strict(cls) -> ContextManager[TAP]:
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        :return: a context decorator
        :rtype: TAP
        """
