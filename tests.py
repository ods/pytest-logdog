import logging


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
