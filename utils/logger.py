import logging
import os
import  datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name=__name__,):
    log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/logs/"
    if not os.path.exists(log_dir):os.makedirs(log_dir)

    log_file = os.path.join(log_dir, datetime.datetime.now().strftime("%Y_%m_%d") + ".log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=64 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
    except PermissionError as e:
        logger.warning(f"无法创建日志文件handler: {e}")
        file_handler = None

    logger.addHandler(console_handler)
    if file_handler:
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
