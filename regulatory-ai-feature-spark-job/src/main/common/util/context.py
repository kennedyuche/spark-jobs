from .settings import Settings
import logging

class Context(object):
    def __init__(self, filename):
        self.settings = Settings(filename)
        self.logger = logging.getLogger()