#!/usr/bin/env python

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

class TestCreation(TestConfig):
    def testLhConfigRun(self):
        assert os.path.exists(os.path.join(self.dir, 'config'))

    def testFailingNewConfiguration(self):
        """
        Should throw IOError for an invalid directory.
        """
        self.assertRaises(IOError, Config, '/proc')

class TestElements(TestConfig):
    def testBinary(self):
        from DebianLive.elements import KeyVar
        self.assertEqual(type(self.lh.binary), KeyVar)

class TestSetGetOptions(TestConfig):
    def testGet(self):
        self.assertEqual(self.lh.common['LH_APT'], 'aptitude')

    def testSet(self):
        self.lh.common['LH_APT'] = 'spam'
        self.assertEqual(self.lh.common['LH_APT'], 'spam')

    def testSetUnknownOption(self):
        self.lh.common['LH_UNKNOWN_OPTION'] = 'spam'
        self.assertEqual(self.lh.common['LH_UNKNOWN_OPTION'], 'spam')

if __name__ == "__main__":
    unittest.main()
