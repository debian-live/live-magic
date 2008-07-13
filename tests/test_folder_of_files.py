#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive.elements import FolderOfFiles

class TestFolderOfFiles(unittest.TestCase):
    name = 'fof-test'

    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, 'config', self.name))
        self.reload()

    def reload(self):
        self.fof = FolderOfFiles(self.dir, 'dummy name', self.name)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir)

    def f_c(self, filename):
        return open(os.path.join(self.dir, 'config', self.name, filename), 'r').read()

    def write(self, filename, contents):
        f = open(os.path.join(self.dir, 'config', self.name, filename), 'w+')
        f.write(contents)
        f.close()

class TestSimple(TestFolderOfFiles):
    def testEmptyFolder(self):
        self.assertEqual(len(self.fof), 0)

    def testSmallFiles(self):
        self.write('spam', 'eggs')
        self.reload()
        self.assertEqual(self.fof['spam'], 'eggs')

    def testNewFile(self):
        self.fof['spam'] = 'eggs'
        self.assertRaises(IOError, self.f_c, 'spam')

    def testIgnoreFoldersInDir(self):
        os.mkdir(os.path.join(self.dir, 'config', self.name, 'dir-name'))
        self.reload()
        self.assertEqual(len(self.fof), 0)

class TestSave(TestFolderOfFiles):
    def testSave(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        self.assertEqual(self.f_c('spam'), 'eggs')

    def testEditFile(self):
        self.write('spam', 'eggs')
        self.reload()
        self.assertEqual(self.f_c('spam'), 'eggs')

        self.fof['spam'] = 'bacon'
        self.fof.save()
        self.assertEqual(self.f_c('spam'), 'bacon')

class TestRename(TestFolderOfFiles):
    def testNoSave(self):
        self.fof['spam'] = 'eggs'

        self.fof['new_name'] = self.fof['spam']
        del self.fof['spam']

        self.assert_('new_name' in self.fof)
        self.assert_('spam' not in self.fof)
        self.assertRaises(IOError, self.f_c, 'spam')
        self.assertRaises(IOError, self.f_c, 'new_name')

    def testOneSave(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()

        self.fof['new_name'] = self.fof['spam']
        del self.fof['spam']

        self.assert_('new_name' in self.fof)
        self.assert_('spam' not in self.fof)
        self.assertEqual(self.f_c('spam'), 'eggs')
        self.assertRaises(IOError, self.f_c, 'new_name')

    def testTwoSaves(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()

        self.fof['new_name'] = self.fof['spam']
        del self.fof['spam']
        self.fof.save()

        self.assert_('new_name' in self.fof)
        self.assert_('spam' not in self.fof)
        self.assertRaises(IOError, self.f_c, 'spam')
        self.assertEqual(self.f_c('new_name'), 'eggs')

class TestDelete(TestFolderOfFiles):
    def testNoSave(self):
        self.fof['spam'] = 'eggs'
        del self.fof['spam']
        self.assert_('spam' not in self.fof)
        self.assertRaises(IOError, self.f_c, 'spam')

    def testDeleteUnsavedItem(self):
        self.fof['spam'] = 'eggs'
        del self.fof['spam']
        self.fof.save()
        self.assert_('spam' not in self.fof)
        self.assertRaises(IOError, self.f_c, 'spam')

    def testSaved(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()
        del self.fof['spam']
        self.fof.save()
        self.assert_('spam' not in self.fof)
        self.assertRaises(IOError, self.f_c, 'spam')

    def testUpdated(self):
        self.fof['spam'] = 'eggs'
        self.fof.save()

        del self.fof['spam']
        self.fof['spam'] = 'bacon'
        self.fof.save()
        self.assertEqual(self.f_c('spam'), 'bacon')

class TestImport(TestFolderOfFiles):
    def setUp(self):
        TestFolderOfFiles.setUp(self)

        import tempfile
        fd, self.filename = tempfile.mkstemp()
        self.conf_name = self.filename.split(os.sep)[-1]
        os.write(fd, 'spam')
        os.close(fd)

    def tearDown(self):
        os.unlink(self.filename)
        TestFolderOfFiles.tearDown(self)

    def testSimple(self):
        self.fof.import_file(self.filename)
        self.fof.save()
        self.assertEqual(self.f_c(self.conf_name), 'spam')

    def testNotSaved(self):
        self.fof.import_file(self.filename)
        self.assertRaises(IOError, self.f_c, self.conf_name)

    def testAlreadyExists(self):
        self.fof[self.conf_name] = 'existing_file'
        self.fof.save()

        self.fof.import_file(self.filename)
        self.fof.save()

        self.assertEqual(self.f_c(self.conf_name), 'existing_file')
        self.assertEqual(self.fof[self.conf_name], 'existing_file')

        self.assertEqual(self.f_c("%s-1" % self.conf_name), 'spam')
        self.assertEqual(self.fof["%s-1" % self.conf_name], 'spam')

    def testAlreadyExistsTwo(self):
        self.fof[self.conf_name] = 'existing_file'
        self.fof.save()

        self.fof.import_file(self.filename)
        self.fof.save()

        self.write(self.filename, 'eggs')
        self.fof.import_file(self.filename)
        self.fof.save()

        self.assertEqual(self.f_c(self.conf_name), 'existing_file')
        self.assertEqual(self.fof[self.conf_name], 'existing_file')

        self.assertEqual(self.f_c("%s-1" % self.conf_name), 'spam')
        self.assertEqual(self.fof["%s-1" % self.conf_name], 'spam')

        self.assertEqual(self.f_c("%s-2" % self.conf_name), 'eggs')
        self.assertEqual(self.fof["%s-2" % self.conf_name], 'eggs')

if __name__ == "__main__":
    unittest.main()
