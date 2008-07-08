from DebianLive import utils

import os
import commands

class Config(object):
    def __init__(self, dir, spec=None, **kwargs):
        self.dir = dir

        if spec is None:
            # Load default field specification
            from spec import spec

        from spec import constructor_args
        for option in kwargs:
            option = option.replace('_', '-')
            if option not in constructor_args:
                raise TypeError, 'Unexpected keyword argument "%s"' % option

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        options = ["--%s='%s'" % (k.replace('_', '-'), v)
            for k, v in kwargs.iteritems()]
        cmd = 'cd "%s"; lh_config --ignore-system-defaults %s' % (os.path.abspath(self.dir),
            ' '.join(options))

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

    def __repr__(self):
        return self.__str__()

    def save(self):
        for elem in self.children.values():
            elem.save()
