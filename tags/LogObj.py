import logging

class LogObj(object):
    @property
    def logger(self):
        name = '.'.join([self.__class__.__name__])
        return logging.getLogger(name)