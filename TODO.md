# To-do list (temporary)

All items here are subject for discussion.

## Tests

* [ ] No race (no records lost) when new records are appended in other thread while being pop-ed.

## Features

### Filters

* [ ] A way to filter by exact value of `level`? `level` + `level_exact`? or `level_ge` + `level_eq`?.

### Other

* [ ] `assert_one_pop()` to pop matching and assert only one.  Is it possible to provide custome error message with similar records?   Or full list if it has limitted size.
* [ ] Add methods like `get_text()` to `LogPile` (note, it's also returned from `filter` and `drain`)?
* [ ] Some way to automate `assert pile.is_empty()`? In `__exit__`?
* [ ] Capture all by default for root (i.e. reset to `NOTSET`)? If so, the fixture itself should have pile interface.
* [ ] Return `LogDog` instance from fixture and provide `__call__` method?  This would simplfy annotation (`def test_smth(logdog: LogDog)` instead of current `def test_smth(logdog: Type[LogDog])`), but it also allow undesirable `with logdog as pile`.  Rename `LogDog` to `LogDocContext` and define `LogDog` with `__call__`?  Export `LogDog` in top-level package to allow `from pytest_logdog import LogDog`?  Or may be enter context and return `Pile` from fixture and provide `__call__` method in it to allow using without `with`?
