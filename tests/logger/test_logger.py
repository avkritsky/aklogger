import pytest

from src.logger import models


def test_logger_save_last_log():
    a = models.Logger(user='avkritsky', project='autoblock', ref='test_logger_save_last_log')

    a.info('test')

    assert a.last_log == models.Record(user='avkritsky',
                                       project='autoblock',
                                       ref='test_logger_save_last_log',
                                       level=models.Level.INFO.value,
                                       mess='test')


def test_level_checked():
    a = models.Logger(user='avkritsky', project='autoblock', ref='test_level_checked', level=1)

    a.info('test INFO level')

    assert a.last_log is None

    a.critical('test critical')

    assert a.last_log.mess == 'test critical'


@pytest.mark.parametrize('ref1, ref2, level1, level2',
                         [
                             ('test_for_debug','test_for_debug1',4,3),
                             ('test_for_warning','test_for_warning1',3,2),
                             ('test_for_info','test_for_info1',2,1),
                             ('test_for_critical','test_for_critical1',1,0),
                             ('test_for_error','test_for_error1',0,-1),
                         ])
def test_for_debug(ref1, ref2, level1, level2):
    a = models.Logger(user='avkritsky', project='autoblock', ref=ref1, level=level1)

    if level1 == 4:
        assert a.debug('test_mess')
    elif level1 == 3:
        assert a.warning('test_mess')
    elif level1 == 2:
        assert a.info('test_mess')
    elif level1 == 1:
        assert a.critical('test_mess')
    elif level1 == 0:
        assert a.error('test_mess')

    assert a.last_log.mess == 'test_mess'

    b = models.Logger(user='avkritsky', project='autoblock', ref=ref2, level=level2)

    if level1 == 4:
        assert not b.debug('rest')
    elif level1 == 3:
        assert not b.warning('rest')
    elif level1 == 2:
        assert not b.info('rest')
    elif level1 == 1:
        assert not b.critical('rest')
    elif level1 == 0:
        assert not b.error('rest')

    assert b.last_log is None


def test_alert_for_not_str_message():
    a = models.Logger(user='avkritsky', project='autoblock', ref='test_alert_for_not_str_message', level=2)

    with pytest.raises(models.NotValidMessage):
        a.info(243)


def test_can_created_exist_logger_by_ref():
    a = models.Logger(user='avkritsky', project='autoblock', ref='test_can_created_exist_logger_by_ref', level=2)
    a.info('test ref')

    b = models.Logger(ref='test_can_created_exist_logger_by_ref')

    assert b.last_log.mess == 'test ref'



def test_get_from_instance_for_already_in_id():
    a = models.Logger(user='avkritsky', project='autoblock', ref='iddqd')
    a.info('test message')

    b = models.Logger(user='avkritsky', project='autoblock', ref='iddqd')
    c = models.Logger(user='avkritsky', project='autoblock', ref='aezakmi')

    assert b.last_log.mess == 'test message'
    assert c.last_log != b.last_log
