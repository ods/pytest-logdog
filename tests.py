import logging

import pytest


pytest_plugins = ["pytest_logdog"]


def test_it_works(logdog):
    with logdog(level=logging.INFO) as pile:
        logging.info("Test")
    assert len(pile) == 1
    [rec] = pile
    assert rec.getMessage() == "Test"


def test_nested(logdog):
    with logdog(level=logging.WARNING) as outer:
        logging.warning("Outer warning 1")

        with logdog(level=logging.INFO) as inner:
            logging.info("Inner info")
            logging.warning("Inner warning")

        logging.warning("Outer warning 2")

    assert outer.messages() == [
        "Outer warning 1",
        "Inner warning",
        "Outer warning 2",
    ]
    assert inner.messages() == [
        "Inner info",
        "Inner warning",
    ]


def test_preset_level(logdog):
    logger = logging.getLogger("mod")
    logger.setLevel(logging.WARNING)

    # Precondition: without it the test in the next block doesn't make sense
    with logdog(level=logging.INFO) as pile:
        logger.info("Silenced")
    assert pile.is_empty()

    with logdog(name="mod", level=logging.INFO) as pile:
        logger.info("Aloud")
    assert pile.messages() == ["Aloud"]


@pytest.mark.parametrize(
    "name, matches",
    [("", False), ("mod", True), ("module", False), ("mod.sub", True)],
)
def test_capture_name(logdog, name, matches):
    with logdog(name="mod") as pile:
        logging.getLogger(name).error("Message")
    assert pile.is_empty() == (not matches)


@pytest.mark.parametrize(
    "name, matches",
    [("", False), ("mod", True), ("module", False), ("mod.sub", True)],
)
def test_filter_drain_name(logdog, name, matches):
    with logdog() as pile:
        logging.getLogger(name).error("Message")

    assert pile.filter(name="mod").is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(name="mod").is_empty() == (not matches)
    assert pile.is_empty() == matches


@pytest.mark.parametrize(
    "log_level, filter_level, matches",
    [
        (logging.DEBUG, logging.INFO, False),
        (logging.DEBUG, logging.DEBUG, True),
        (logging.DEBUG, logging.NOTSET, True),
        (logging.DEBUG, "DEBUG", True),
        (logging.DEBUG, 5, True),
        (logging.DEBUG, 15, False),
    ],
)
def test_filter_drain_level(logdog, log_level, filter_level, matches):
    with logdog(level=logging.NOTSET) as pile:
        logging.log(log_level, "Message")

    assert pile.filter(level=filter_level).is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(level=filter_level).is_empty() == (not matches)
    assert pile.is_empty() == matches


@pytest.mark.parametrize(
    "pattern, matches",
    [
        ("^one", True),
        ("two", True),
        ("^two", False),
        ("one.*three", True),
    ],
)
def test_filter_drain_message(logdog, pattern, matches):
    with logdog() as pile:
        logging.error("one two three")

    assert pile.filter(message=pattern).is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(message=pattern).is_empty() == (not matches)
    assert pile.is_empty() == matches


@pytest.mark.parametrize(
    "exc_info, matches",
    [
        (None, True),
        (False, False),
        (True, True),
        (0, False),
        (1, True),
        (object(), True),
        (ZeroDivisionError, True),
        (Exception, True),
        (RuntimeError, False),
        ((ValueError, ArithmeticError), True),
        ((ValueError, TypeError), False),
    ],
)
def test_filter_drain_exc_info_exception(logdog, exc_info, matches):
    with logdog() as pile:
        try:
            1 / 0
        except:
            logging.exception("Error")

    assert pile.filter(exc_info=exc_info).is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(exc_info=exc_info).is_empty() == (not matches)
    assert pile.is_empty() == matches


@pytest.mark.parametrize(
    "exc_info, matches",
    [
        (None, True),
        (False, True),
        (True, False),
        (0, True),
        (1, False),
        (object(), False),
        (Exception, False),
        ((ValueError, TypeError), False),
    ],
)
def test_filter_drain_exc_info_no_exception(logdog, exc_info, matches):
    with logdog() as pile:
        logging.error("Error")

    assert pile.filter(exc_info=exc_info).is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(exc_info=exc_info).is_empty() == (not matches)
    assert pile.is_empty() == matches


@pytest.mark.parametrize(
    "log_stack_info, filter_stack_info, matches",
    [
        (None, None, True),
        (False, None, True),
        (True, None, True),
        (None, False, True),
        (None, True, False),
        (False, False, True),
        (False, 0, True),
        (False, True, False),
        (False, 1, False),
        (False, object(), False),
        (True, False, False),
        (True, 0, False),
        (True, True, True),
        (True, 1, True),
        (True, object(), True),
    ],
)
def test_filter_drain_stack_info(
    logdog, log_stack_info, filter_stack_info, matches
):
    with logdog() as pile:
        logging.error("Error", stack_info=log_stack_info)

    assert pile.filter(stack_info=filter_stack_info).is_empty() == (not matches)
    assert not pile.is_empty()

    assert pile.drain(stack_info=filter_stack_info).is_empty() == (not matches)
    assert pile.is_empty() == matches
