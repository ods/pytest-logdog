import logging


pytest_plugins = ['pytest_logdog']


def test_it_works(logdog):
    with logdog(level=logging.INFO) as pile:
        logging.info('Test')
    assert len(pile) == 1
    [rec] = pile
    assert rec.getMessage() == 'Test'
