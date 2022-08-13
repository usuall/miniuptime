import logging


def set_Logger(log_level):
    # 로그 레벨정의
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    debug_file = 'miniuptime.log'
    file_handler = logging.FileHandler(debug_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter('%(asctime)s (%(levelname)s) %(message)s')

    logger = logging.getLogger('miniuptime')
    logger.addHandler(file_handler)
