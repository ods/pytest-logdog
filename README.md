# pytest-logdog: Pytest plugin to test logging

## Usage

```python
pytest_plugins = ["pytest_logdog"]

def test_it_works(logdog):
    with logdog() as pile:
        logging.info("Hello world!")
    [rec] = pile.drain(message="Hello.*")
    assert rec.levelno == logging.INFO
    assert pile.is_empty()
```


## Links

* [Rationale and design](https://github.com/ods/pytest-logdog/blob/master/DESIGN.md)
* [Change log](https://github.com/ods/pytest-logdog/blob/master/CHANGELOG.md)
