#!/usr/bin/env python

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive.utils import get_build_dir

class TestUtils(unittest.TestCase):
    def testBuildDir(self):
        self.assertEqual(type(get_build_dir()), str)
        self.assert_(len(get_build_dir()) > 0)

if __name__ == "__main__":
    unittest.main()
