import logging

PROJECT_TAG = 'kafka_Secedgar'
info_logger = lambda i: logging.info(f'{PROJECT_TAG}: {i}')
error_logger = lambda i: logging.error(f'{PROJECT_TAG}: {i}')


class Logger(object):
    def getLogger(self, prefix, project):
        logger = logging.getLogger(PROJECT_TAG)
        # formatter = logging.Formatter('%(prefix)s : %(messages)s')
        # file_handler = logging.FileHandler("handler.log")
        # logger.addHandler(file_handler)
        return logger
