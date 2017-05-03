__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'


class GamsAddOnException(Exception):
    def __init__(self, message):
        super(GamsAddOnException, self).__init__(message)
        self.message = message
