"""Test Anything Protocol tools."""

from contextlib import ContextDecorator
from contextlib import contextmanager
from typing import Any
from typing import Generator
from typing import NoReturn

OK = ...
NOT_OK = ...
SKIP = ...
class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Subtests are not implemented.

    .. note::
        Not known to be thread-safe.
    """
    _formatwarning = ...
    _showwarning = ...
    _count = ...
    @classmethod
    def end(cls, skip_reason: str = ...) -> NoReturn:
        """End a TAP diagnostic.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        :return: Exits the diagnostic.
        :rtype: NoReturn
        """

    @staticmethod
    def diagnostic(*message: str) -> None:
        r"""Print a diagnostic message.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        r"""Print a bail out message and exit.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """

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



