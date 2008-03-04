#!/usr/bin/env python

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive.utils import SourcesList

class TestSourcesList(unittest.TestCase):
    def setUp(self):
        import tempfile
        fd, self.filename = tempfile.mkstemp('live-magic')
        os.close(fd)
        self.s = SourcesList(self.filename)

    def tearDown(self):
        os.unlink(self.filename)

    def f_w(self, contents):
        f = open(self.filename, 'w+')
        f.write(contents)
        f.close()

class TestMatch(TestSourcesList):
    def assertMatchLine(self, line):
        self.f_w(line)
        self.assert_(self.s.get_mirror(None))

    def testCountryDebianMirror(self):
        self.assertMatchLine('deb http://ftp.uk.debian.org/debian stable main')

    def testDebianMirror(self):
        self.assertMatchLine('deb http://ftp.debian.org/debian stable main')

    def testLocalhost(self):
        self.assertMatchLine('deb http://localhost/debian stable main')

    def testOtherURL(self):
        self.assertMatchLine('deb http://the.earth.li/debian stable main')

class TestNoMatch(TestSourcesList):
    def assertNoMatchLine(self, line):
        self.f_w(line)
        self.failIf(self.s.get_mirror(None))

    def testSecurity(self):
        self.assertNoMatchLine('deb http://security.debian.org/debian stable main')

    def testBackports(self):
        self.assertNoMatchLine('deb http://backports.debian.org/debian stable main')

"""
# Not implemented yet

class Prefer(TestSourcesList):
    def assertPrefer(self, *ordering):
        def test():
            self.f_w(""""""
                deb %s stable main
                deb %s stable main
            """""" % (ordering[0], ordering[1]))

            self.assertEqual(self.s.get_mirror(), ordering[0])

        test()
        ordering.reverse()
        self.setUp()
        test()

    def testPreferLocalhost(self):
        self.assertPrefer('http://localhost/debian', 'http://ftp.uk.debian.org/debian')

    def testPreferCountry(self):
        self.assertPrefer('http://ftp.uk.debian.org/debian', 'http://ftp.debian.org/debian')

    def testPreferNonOfficial(self):
        self.assertPrefer('http://ftp.uk.debian.org/debian', 'http://backports.debian.org/debian')
"""

if __name__ == "__main__":
    unittest.main()
