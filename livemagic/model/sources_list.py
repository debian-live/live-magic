import os
import re

class SourcesList(object):
    """
    Represents /etc/apt/sources.list
    """

    def __init__(self, filename=None):
        if filename is None:
            self.filename = r'/etc/apt/sources/list'
        else:
            self.filename = filename

    def get_mirror(self):
        result = r'http://ftp.us.debian.org/'

        try:
            f = open(self.filename, 'r')
            for line in f.readlines():
                pass
        finally:
            f.close()

        return result
