from contextlib import contextmanager
import logging

import pytest


class LogPile:
    __slots__ = ('_records',)

    def __init__(self):
        self._records = []

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return iter(self._records)


class LogHandler(logging.Handler):
    __slots__ = ('_pile',)

    def __init__(self, pile):
        self._pile = pile

    def handle(self, record):
        self._pile._records.append(record)


class LogDog:
    __slots__ = ('_logger', '_handler', '_orig_level', '_level')

    def __init__(self, name=None, level=None):
        self._logger = logging.getLogger(name)
        self._level = level

    def __enter__(self):
        pile = LogPile()
        self._handler = LogHandler(pile)
        if self._level is not None:
            self._handler.setLevel(self._level)

        self._logger.addHandler(self._handler)

        if self._level is not None:
            self._orig_level = self._logger.level
            # Argument `level` can be `None`, `int` or `str`, while
            # `handler.level` is always `int` (converted by `setLevel()`
            # method)
            self._logger.setLevel(min(self._orig_level, self._handler.level))

        return pile

    def __exit__(self, type, value, traceback):
        if self._level is not None:
            self._logger.setLevel(self._orig_level)

        self._logger.removeHandler(self._handler)


@pytest.fixture
def logdog():
    return LogDog
