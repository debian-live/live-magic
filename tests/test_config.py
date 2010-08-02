#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2010 Chris Lamb <lamby@debian.org>
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

from DebianLive import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()
        self.lh = Config(self.dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir)

class TestSimple(TestConfig):
    def testLhConfigRun(self):
        assert os.path.exists(os.path.join(self.dir, 'config'))

    def testFailingNewConfiguration(self):
        self.assertRaises(IOError, Config, '/proc')

    def testNoDirectory(self):
        self.tearDown()
        Config(self.dir)

    def testStr(self):
        self.assertEqual(type(str(self.lh)), str)

    def testRepr(self):
        self.assertEqual(type(repr(self.lh)), str)

    def testStrReprEquality(self):
        self.assertEqual(repr(self.lh), str(self.lh))

    def testSave(self):
        def contents():
            return open(os.path.join(self.dir, 'config', 'common')).readlines()

        before = contents()
        self.lh.common['LH_APT'] = 'spam'
        self.lh.save()

        self.assert_('LH_APT="spam"\n' in contents())
        self.assertEqual(len(before), len(contents()))

class TestElements(TestConfig):
    def testBinary(self):
        from DebianLive.elements import KeyVar
        self.assertEqual(type(self.lh.binary), KeyVar)

class TestSetGetOptions(TestConfig):
    def testGet(self):
        self.assertEqual(self.lh.common['LH_DEBCONF_PRIORITY'], 'critical')

    def testSet(self):
        self.lh.common['LH_APT'] = 'spam'
        self.assertEqual(self.lh.common['LH_APT'], 'spam')

    def testSetUnknownOption(self):
        self.lh.common['LH_UNKNOWN_OPTION'] = 'spam'
        self.assertEqual(self.lh.common['LH_UNKNOWN_OPTION'], 'spam')

if __name__ == "__main__":
    unittest.main()
