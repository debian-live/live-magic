import os

def find_resource(resource):
    dirs = (
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'misc'),
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '/usr/bin',
        '/usr/local/bin',
        '/usr/share/live-magic',
        '/usr/local/share/live-magic',
        '/usr/share/common-licenses',
    )

    tried = []
    for base in dirs:
        path = os.path.join(base, resource)
        if os.path.isfile(path):
            return path
        tried.append(path)

    raise ValueError, 'Cannot find %s resource. Tried: %s' % (resource, tried)
