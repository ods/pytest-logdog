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

* [ ] By `level` (None, int, str), greater or equal (or `level_eq` + `level_ge`?).
* [ ] By `exc_info` (None, bool, class, tuple of classes or tuples).
* [ ] By `stack_info` (optional bool).

### Other

* [x] Better name for `find()`? `get()` (this looks better without args, but might be mistakenly assumed to return single item)?
* [ ] `assert_pop_one()` to pop matching and assert only one.  Is it possible to provide custome error message with similar records?   Or full list if it has limitted size.
* [ ] `assert_pop()`?
* [ ] Return pile from filters instead of list? Provide methods like `get_text()`?
* [ ] Some way to automate `assert pile.empty()`? In `__exit__`? In `__del__`?
* [ ] Capture all by default for root (i.e. reset to `NOTSET`)?
