import logging

DEFAULT_LOG_FORMAT = '{asctime} [{process}] {levelname:5} {name}: {message}'


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter(DEFAULT_LOG_FORMAT, style='{')
    )
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stream_handler())
    return logger
