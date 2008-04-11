#!/usr/bin/env python

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive import Config

class TestConfigConstructor(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir)

class TestSimple(TestConfigConstructor):
    def testArch386(self):
        lh = Config(self.dir, architecture='i386')
        self.assertEqual(lh.bootstrap['LH_ARCHITECTURE'], 'i386')

    def testArchAmd64(self):
        lh = Config(self.dir, architecture='amd64')
        self.assertEqual(lh.bootstrap['LH_ARCHITECTURE'], 'amd64')

    def testNoOptions(self):
        lh = Config(self.dir)

    def testInvalid(self):
        self.assertRaises(TypeError, Config, self.dir, this_config_never_exists='value')

class TestOther(TestConfigConstructor):
    def testArchChangesKernelFlavour(self):
        lh_i386 = Config(self.dir, architecture='i386')
        self.setUp()
        lh_amd64 = Config(self.dir, architecture='amd64')
        self.assertNotEqual(lh_i386.chroot['LH_LINUX_FLAVOURS'],
            lh_amd64.chroot['LH_LINUX_FLAVOURS'])

    def testHyphenatedOption(self):
        lh = Config(self.dir, packages_lists='my-package-list')
        self.assertEqual(lh.chroot['LH_PACKAGES_LISTS'], ['my-package-list'])

    def testSpaceInValue(self):
        lh = Config(self.dir, packages_lists="hello there")
        self.assertEqual(lh.chroot['LH_PACKAGES_LISTS'], ['hello', 'there'])

if __name__ == "__main__":
    unittest.main()
