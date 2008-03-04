import os
import re

class SourcesList(object):
    comments = re.compile(r'\s*#')
    patterns = (
        re.compile(r'http://ftp.?\..{2}\.debian\.org[^\s]*'),
        re.compile(r'http://(localhost|127\.0\.0\.1)[^\s]*'),
        re.compile(r'http://[^\s]*'),
    )
    reject_patterns = (
        re.compile(r'backports\.'),
        re.compile(r'security\.'),
    )

    def __init__(self, filename=None):
        if filename is None:
            filename = r'/etc/apt/sources.list'

        self.filename = filename

    def get_mirror(self, fallback=None):
        if fallback is not None:
            fallback = 'http://www.us.debian.org/'

        result = fallback

        f = open(self.filename, 'r')
        try:
            try:
                for line in f.readlines():
                    if self.comments.match(line):
                        continue

                    flag = False
                    for pat in self.reject_patterns:
                        m = pat.search(line)
                        if m:
                            flag = True
                            break
                    if flag:
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
