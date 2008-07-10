import os
import re

from DebianLive.elements import KeyVar

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

def get_mirror(fallback='http://www.us.debian.org/', sources_list='/etc/apt/sources.list', defaults='/etc/default/live-helper'):
    result = fallback

    def filter_mirror(line):
        if COMMENTS.match(line):
            return False

        for pat in REJECT_PATTERNS:
            m = pat.search(line)
            if m:
                return False

        for pat in PATTERNS:
            m = pat.search(line)
            if m:
                return m.group(0)

        return False

    try:
        f = open(sources_list, 'r')
        try:
            for line in f.readlines():
                mirror = filter_mirror(line)
                if mirror:
                    result = mirror
                    break
        finally:
            f.close()
    except IOError:
        pass

    if defaults:
        try:
            kv = KeyVar('/etc/default', 'live-helper', {}, filename=defaults)
            kv_mirror = filter_mirror(kv['LH_MIRROR_BOOTSTRAP'])
            if kv_mirror:
                return kv_mirror
        except:
            pass

    return result
