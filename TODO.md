# To-do list (temporary)

All items here are subject for discussion.

## Tests

* [x] Interference in nested scopes.
* [x] Capturing for logger with level set by default.
* [ ] No race (no records lost) when new records are appended in other thread while being pop-ed.
* [ ] `filter`/`drain` with each filters and combinations, including:
    * [x] `name` is equal and parent, empty string is equivalent to `None`.
    * [x] `message` from start, in the middle etc.
    * [ ] Different variants of `exc_info`.

## Features

### Filters

* [x] By `level` (None, int, str), greater or equal (or `level` + `level_exact`? or `level_ge` + `level_eq`?).
* [ ] By `exc_info` (None, bool, class, tuple of classes or tuples).
* [ ] By `stack_info` (optional bool).

### Other

* [x] Better name for `find()`?
* [ ] `assert_one_pop()` to pop matching and assert only one.  Is it possible to provide custome error message with similar records?   Or full list if it has limitted size.
* [ ] Return pile from filters instead of list? Provide methods like `get_text()`?
* [ ] Some way to automate `assert pile.empty()`? In `__exit__`? In `__del__`?
* [ ] Capture all by default for root (i.e. reset to `NOTSET`)?
* [ ] Return `LogDog` instance from fixture and provide `__call__` method?  This would simplfy annotation (`def test_smth(logdog: LogDog)` instead of current `def test_smth(logdog: Type[LogDog])`), but it also allow undesirable `with logdog as pile`.  Rename `LogDog` to `LogDocContext` and define `LogDog` with `__call__`?  Export `LogDog` in top-level package to allow `from pytest_logdog import LogDog`?  Or may be enter context and return `Pile` from fixture and provide `__call__` method in it to allow using without `with`?
