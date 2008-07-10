import os
import re

__all__ = ['get_mirror']

COMMENTS = re.compile(r'\s*#')
PATTERNS = (
    re.compile(r'http://ftp.?\..{2}\.debian\.org[^\s]*'),
    re.compile(r'http://(localhost|127\.0\.0\.1)[^\s]*'),
    re.compile(r'http://[^\s]*'),
)
REJECT_PATTERNS = (
    re.compile(r'backports\.'),
    re.compile(r'security\.'),
)

def get_mirror(fallback='http://www.us.debian.org/', sources_list='/etc/apt/sources.list'):
    result = fallback

    try:
        f = open(sources_list, 'r')

        try:
            for line in f.readlines():
                if COMMENTS.match(line):
                    continue

                flag = False
                for pat in REJECT_PATTERNS:
                    m = pat.search(line)
                    if m:
                        flag = True
                        break
                if flag:
                    continue

                for pat in PATTERNS:
                    m = pat.search(line)
                    if not m:
                        continue

                    result = m.group(0)
        finally:
            f.close()
    except IOError:
        pass

    return result
