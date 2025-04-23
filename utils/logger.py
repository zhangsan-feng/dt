import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)


# file_handler = RotatingFileHandler(
#     'app.log', maxBytes=5 * 1024 * 1024, backupCount=3
# )
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
#
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)