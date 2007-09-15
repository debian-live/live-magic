#!/usr/bin/env python

import unittest
import tempfile
import os

import sys
sys.path.append('..')
from livemagic import model

class TestFolderOfFiles(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp('live-magic')
        self.fof = model.FolderOfFiles(self.dir)

    def f_c(self, filename):
        return open("%s/%s" % (self.dir, filename), 'r').read()

    def write(self, filename, contents):
        f = open("%s/%s" % (self.dir, filename), 'w+')
        f.write(contents)
        f.close()

    def testEmptyFolder(self):
        assert len(self.fof.files) == 0

    def testSmallFiles(self):
        self.write('one', 'Contents of file one')
        self.write('two', 'Contents of file two')
        self.fof.load()
        assert self.fof['one'] == 'Contents of file one'
        assert self.fof['two'] == 'Contents of file two'

    def testnewfile(self):
        self.fof['spam'] = 'eggs'
        self.assertRaises(IOError, self.f_c, 'spam')

    def testSave(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        assert self.f_c('spam') == 'eggs'

    def testEditFile(self):
        self.write('spam', 'eggs')
        self.fof.load()
        assert self.f_c('spam') == 'eggs'
        self.fof['spam'] = 'moreeggs'
        self.fof.save()
        assert self.f_c('spam') == 'moreeggs'

    def testAlteredState(self):
        assert self.fof.altered() == False
        self.fof['spam'] = 'eggs'
        assert self.fof.altered() == True
        self.fof.save()
        assert self.fof.altered() == False

    def testNewRename(self):
        self.fof['spam'] = 'eggs'
        self.fof.rename('spam', 'morespam')
        assert 'morespam' in self.fof
        assert 'spam' not in self.fof
        self.assertRaises(IOError, self.f_c, 'morespam')
        self.assertRaises(IOError, self.f_c, 'spam')

    def testAlteredStateNewRename(self):
        self.fof['spam'] = 'eggs'
        assert self.fof.altered() == True
        self.fof.rename('spam', 'morespam')
        assert self.fof.altered() == True

    def testExistingRename(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        self.fof.rename('spam', 'morespam')
        assert 'morespam' in self.fof
        assert 'spam' not in self.fof
        assert self.f_c('morespam') == 'eggs'
        self.assertRaises(IOError, self.f_c, 'spam')

    def testRenameFileExists(self):
        self.fof['spam'] = 'eggs'
        self.fof['morespam'] = 'moreeggs'
        self.fof.save()
        try:
            self.fof.rename('spam', 'morespam')
            self.fail(msg="Should have thrown ValueError on a renaming overwrite")
        except ValueError:
            pass

    def testAlteredStateRename(self):
        self.fof['spam'] = 'eggs'
        assert self.fof.altered() == True
        self.fof.save()
        assert self.fof.altered() == False
        self.fof.rename('spam', 'morespam')
        assert self.fof.altered() == True

    def testDeleteNotSaved(self):
        self.fof['spam'] = 'eggs'
        self.assertRaises(IOError, self.f_c, 'spam')
        assert 'spam' in self.fof
        self.fof.delete('spam')
        assert 'spam' not in self.fof

    def testDeleteNotSavedAlteredState(self):
        assert self.fof.altered() == False
        self.fof['spam'] = 'eggs'
        assert self.fof.altered() == True
        self.fof.delete('spam')
        assert self.fof.altered() == True

    def testDeleteSaved(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        assert self.f_c('spam') == 'eggs'
        self.fof.delete('spam')
        self.assertRaises(IOError, self.f_c, 'spam')

    def testDeleteSavedAlteredState(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        assert self.fof.altered() == False
        self.fof.delete('spam')
        assert self.fof.altered() == True
        self.assertRaises(IOError, self.f_c, 'spam')

    def testIgnoreFoldersInDir(self):
        os.mkdir("%s/spam" % self.dir,)
        self.fof.load()
        assert len(self.fof.files) == 0

    def testImportFile(self):
        fd, filename = tempfile.mkstemp('live-magic')
        conf_name = filename.split(os.sep)[-1]
        os.write(fd, 'spam')
        os.close(fd)
        self.fof.import_file(filename)
        self.fof.save()
        assert self.f_c(conf_name) == 'spam'

    def testImportFileNotSaved(self):
        fd, filename = tempfile.mkstemp('live-magic')
        conf_name = filename.split(os.sep)[-1]
        os.write(fd, 'spam')
        os.close(fd)
        self.fof.import_file(filename)
        self.assertRaises(IOError, self.f_c, conf_name)

    def testImportAlreadyExists(self):
        fd, filename = tempfile.mkstemp('live-magic')
        conf_name = filename.split('/')[-1]
        os.write(fd, 'file_to_import')
        os.close(fd)

        self.fof[conf_name] = 'existing_file'
        self.fof.save()

        self.fof.import_file(filename)
        self.fof.save()
        assert self.f_c(conf_name) == 'existing_file'
        self.fof[conf_name] == 'existing_file'
        assert self.f_c("%s-1" % conf_name) == 'file_to_import'
        self.fof["%s-1" % conf_name] == 'file_to_import'

if __name__ == "__main__":
    unittest.main()
