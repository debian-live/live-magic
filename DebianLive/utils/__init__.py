from sources_list import SourcesList
from list_observer import ListObserver

import os.path
import time

def get_build_dir():
    return os.path.expanduser('~/DebianLive/%s' % time.strftime('%Y-%m-%d-%H%M%S'))
