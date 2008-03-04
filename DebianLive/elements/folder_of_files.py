import glob
import os

from os.path import join

class FolderOfFiles(dict):
    """
    Represents a folder containing a number of files.
    """

    def __new__(self, *args, **kwargs):
        return dict.__new__(self, *args, **kwargs)

    def __init__(self, basedir, name, dir):
        self.dir = os.path.join(basedir, 'config', dir)

        self.stale = set()

        for name in glob.glob(join(self.dir, '*')):
            key = name.split('/')[-1]
            try:
                f = open(name, 'r')
                try:
                    dict.__setitem__(self, key, f.read())
                finally:
                    f.close()
            except IOError, e:
                # "Is a directory"
                if e.errno == 21:
                    continue
                raise e

    def __delitem__(self, k):
        self.stale.add(k)
        dict.__delitem__(self, k)

    def __setitem__(self, k, v):
        self.stale.add(k)
        dict.__setitem__(self, k, v)

    def _config_exists(self, file):
        try:
            os.stat(join(self.dir, file))
            return True
        except OSError:
            return False

    def save(self):
        for filename in self.stale:
            if filename in self:
                pathname = join(self.dir, filename)

                f = open(pathname, 'w+')
                try:
                    f.write(self[filename])
                finally:
                    f.close()
            else:
                if self._config_exists(filename):
                    os.remove(join(self.dir, filename))
        self.stale.clear()

    def import_file(self, source):
        """
        Imports the specified file into the current configuration, using a
        unique name. The file is not saved.
        """
        f = open(source, 'r')
        source_contents = f.read()
        f.close()

        def gen_import_name(filename):
            # Use existing filename as the root
            root = filename.split(os.sep)[-1]

            if root not in self:
                return root

            i = 1
            while True:
                tmpnam = "%s-%d" % (root, i)
                if not tmpnam in self:
                    return tmpnam
                i += 1

        target_name = gen_import_name(source)
        self[target_name] = source_contents

        return target_name
