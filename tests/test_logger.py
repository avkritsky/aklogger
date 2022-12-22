import pytest

from models import logger
from models import record


def test_logger_save_last_log():
    a = logger.Logger(user='avkritsky', project='autoblock', ref='test_logger_save_last_log')

    a.info('test')

    assert a.last_log == record.Record(user='avkritsky',
                                       project='autoblock',
                                       ref='test_logger_save_last_log',
                                       level=record.Level.INFO.value,
                                       mess='test')


def test_level_checked():
    a = logger.Logger(user='avkritsky', project='autoblock', ref='test_level_checked', level=1)

    a.info('test INFO level')

    assert a.last_log is None

    a.critical('test critical')

    assert a.last_log.mess == 'test critical'


def test_alert_for_not_str_message():
    a = logger.Logger(user='avkritsky', project='autoblock', ref='test_alert_for_not_str_message', level=2)

    with pytest.raises(logger.NotValidMessage):
        a.info(243)


def test_can_created_exist_logger_by_ref():
    a = logger.Logger(user='avkritsky', project='autoblock', ref='test_can_created_exist_logger_by_ref', level=2)
    a.info('test ref')

    b = logger.Logger(ref='test_can_created_exist_logger_by_ref')

    assert b.last_log.mess == 'test ref'



def test_get_from_instance_for_already_in_id():
    a = logger.Logger(user='avkritsky', project='autoblock', ref='iddqd')
    a.info('test message')

    b = logger.Logger(user='avkritsky', project='autoblock', ref='iddqd')
    c = logger.Logger(user='avkritsky', project='autoblock', ref='aezakmi')

    assert b.last_log.mess == 'test message'
    assert c.last_log != b.last_log
