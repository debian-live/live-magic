import glob
import os

from os.path import join

class FolderOfFiles(object):
    """
    Represents a folder containing a number of files.
    """

    def __init__(self, basedir, name, dir):
        self.dir = os.path.join(basedir, 'config', dir)

        self._stale = set()
        self.files = {}

        # No file has been deleted
        self.file_deleted = False

        self.load()

    def __getitem__(self, k):
        return self.files[k]

    def __contains__(self, k):
        return k in self.files

    def __delitem__(self, k):
        del self.files[k]

    def __setitem__(self, k, v):
        self._stale.add(k)
        self.files[k] = v

    def _config_exists(self, file):
        try:
            os.stat(join(self.dir, file))
            return True
        except OSError:
            return False

    def load(self):
        """
        Loads files.
        """
        self.deleted = False
        self._stale.clear()
        self.files.clear()
        for name in glob.glob(join(self.dir, '*')):
            key = name.split('/')[-1]
            try:
                f = open(name, 'r')
                self.files[key] = f.read()
                f.close()
            except IOError, e:
                # "Is a directory"
                if e.errno == 21:
                    continue
                raise e

    def save(self):
        """
        Update all updated files in this directory.
        """
        for filename in self._stale:
            pathname = join(self.dir, filename)
            f = open(pathname, 'w+')
            f.write(self[filename])
            f.close()

        self._stale.clear()

    def delete(self, hook_name):
        if self._config_exists(hook_name):
            os.remove(join(self.dir, hook_name))
        del self[hook_name]
        if hook_name in self._stale: self._stale.remove(hook_name)
        self.file_deleted = True

    def rename(self, orig, new):
        """
        Throws ValueError if 'new' already exists.
        """
        if self._config_exists(new):
            raise ValueError
        if self._config_exists(orig):
            os.rename(join(self.dir, orig), join(self.dir, new))
        if orig in self._stale: self._stale.remove(orig)
        self[new] = self[orig]
        del self[orig]

    def import_file(self, source):
        """
        Imports the specified file into the current configuration, using a
        unique name. The file is not saved.
        """
        f = open(source, 'r')
        source_contents = f.read()
        f.close()

        target_name = self._gen_import_name(source)
        self[target_name] = source_contents

        return target_name

    def _gen_import_name(self, filename):
        """
        Generates a unique name of the imported file.
        """
        # Use existing filename as the root
        root = filename.split(os.sep)[-1]

        if root in self:
            # Keep adding a number to the end until it doesn't exist.
            i = 1
            while True:
                tmpnam = "%s-%d" % (root, i)
                if not tmpnam in self:
                    return tmpnam
                i += 1
        else:
            # Just use the root name
            return root
