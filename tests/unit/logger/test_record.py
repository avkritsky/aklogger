from src.logger.record import Record


def test_new_record():
    a = Record(user='avkritsky',
               project='autoblock',
               ref='test_logger_save_last_log',
               level=4,
               mess='test')

    assert a.mess == 'test'
    assert a.level == 4


def test_byting_record():
    a = Record(user='avkritsky',
               project='autoblock',
               ref='test_logger_save_last_log',
               level=4,
               mess='test')

    assert a == Record.from_bytes(a.rebytes)