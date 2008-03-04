from DebianLive import utils

import os
import commands

class Config(object):
    def __init__(self, dir, spec=None):
        self.dir = dir

        if spec is None:
            # Load default field specification
            from spec import spec

        # Create skeleton lh_config dir, if it does not already exist
        if not os.path.exists(os.path.join(self.dir, 'config')):
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            cmd = 'cd "%s"; lh_config' % os.path.abspath(self.dir)
            result, out = commands.getstatusoutput(cmd)
            if result != 0:
                raise IOError, out

        self.children = {}
        for name, details in spec.iteritems():
            elem_type = details[0]
            elem = elem_type(self.dir, name, *details[1:])
            self.children[name] = elem
            setattr(self, name, elem)

    def __str__(self):
        from pprint import pformat
        return '<DebianLive.Config dir="%s" %s>' % (self.dir, pformat(self.children))

    def save(self):
        for elem in self.children.values():
            elem.save()
