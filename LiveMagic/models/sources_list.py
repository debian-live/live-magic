import os
import re

class SourcesList(object):
    """
    Represents /etc/apt/sources.list
    """

    comments = re.compile(r'\s*#')
    patterns = (
        re.compile(r'http://ftp.?\..{2}\.debian\.org[^\s]*'),
        re.compile(r'http://(localhost|127\.0\.0\.1)[^\s]*'),
        re.compile(r'http://[^\s]*'),
    )

    def __init__(self, filename=None):
        if filename is None:
            self.filename = r'/etc/apt/sources.list'
        else:
            self.filename = filename

    def get_mirror(self):
        result = r'http://ftp.us.debian.org/'

        f = open(self.filename, 'r')
        try:
            try:
                for line in f.readlines():

                    if self.comments.match(line):
                        continue

                    for pat in self.patterns:
                        m = pat.search(line)
                        if not m:
                            continue

                        result = m.group(0)

            finally:
                f.close()
        except IOError:
            pass

        return result
