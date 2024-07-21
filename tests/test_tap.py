# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import pytest

from tap_producer import TAP  # pyright: ignore


def test_plan_called_gt_once() -> None:  # noqa: DC102, RUF100
    TAP.plan(count=1, skip_count=0)
    TAP.ok('reason')
    TAP.plan(count=1, skip_count=0)

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan() -> None:  # noqa: DC102, RUF100
    TAP.plan(count=1, skip_count=0)
    TAP.ok('reason')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_contextdecorator_all_kwargs() -> None:  # noqa: DC102, RUF100
    @TAP(plan=1, version=14)
    def f() -> None:
        TAP.ok('reason')

    f()
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_contextdecorator_plan() -> None:  # noqa: DC102, RUF100
    @TAP(plan=1)
    def f() -> None:
        TAP.ok('reason')

    f()
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_contextdecorator_version() -> None:  # noqa: DC102, RUF100
    @TAP(version=14)
    def f() -> None:
        TAP.ok('reason')

    f()
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_contextdecorator() -> None:  # noqa: DC102, RUF100
    @TAP()
    def f() -> None:
        TAP.ok('reason')

    f()
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan_v_invalid() -> None:  # noqa: DC102, RUF100
    TAP.version(11)
    TAP.plan(count=1, skip_count=0)
    TAP.ok('reason')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan_v12() -> None:  # noqa: DC102, RUF100
    TAP.version(12)
    TAP.comment('comment')
    TAP.plan(count=1, skip_count=0)
    TAP.ok('reason')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan_v13() -> None:  # noqa: DC102, RUF100
    TAP.version(13)
    TAP.comment('comment')
    TAP.plan(count=1, skip_count=0)
    TAP.ok('reason')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan_v14() -> None:  # noqa: DC102, RUF100
    TAP.version(14)
    TAP.version(14)
    TAP.comment('comment')
    TAP.plan(count=1, skip_count=0)
    with TAP.subtest('subtest'):
        TAP.plan(count=1, skip_count=0)
        TAP.ok('ok')
    with TAP.subtest('subtest2'):
        TAP.ok('ok')

    with pytest.raises(RuntimeWarning):  # noqa: PT012, RUF100
        with TAP.subtest('subtest3'):
            TAP.not_ok('not ok')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_plan_no_skip_count() -> None:  # noqa: DC102, RUF100
    TAP.plan(count=1, skip_count=None)
    TAP.ok('reason')

    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_end_skip() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_bail_out() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.bail_out()
    TAP._count.clear()  # noqa: SLF001


def test_end_skip_reason() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.end('reason')
    TAP._count.clear()  # noqa: SLF001


def test_producer_ok() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes')
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_ok_skip_reason() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes')
    with pytest.raises(SystemExit):
        TAP.end('reason')
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_ok() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes', skip=True)
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_ok_with_reason() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes', skip=True)
    with pytest.raises(SystemExit):
        TAP.end('Skip pass reason.')
    TAP._count.clear()  # noqa: SLF001


def test_producer_not_ok() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails')
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_not_ok() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails', skip=True)
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_not_ok_with_reason() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails', skip=True)
    with pytest.raises(SystemExit):
        TAP.end('Skip fail reason.')
    TAP._count.clear()  # noqa: SLF001
