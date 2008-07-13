#!/usr/bin/env python

import unittest
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive.utils import get_mirror

class TestSourcesList(unittest.TestCase):
    def setUp(self):
        import tempfile
        fd, self.filename = tempfile.mkstemp('live-magic')
        os.close(fd)

    def tearDown(self):
        try:
            os.unlink(self.filename)
        except OSError:
            pass

    def f_w(self, contents, filename=None):
        if filename is None:
            f = open(self.filename, 'w+')
        else:
            f = open(filename, 'w+')
        f.write(contents)
        f.close()

class TestMatch(TestSourcesList):
    def assertMatchLine(self, line):
        self.f_w(line)
        self.assert_(get_mirror(None, sources_list=self.filename, defaults=None))

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
        self.failIf(get_mirror(None, sources_list=self.filename, defaults=None))

    def testComments(self):
        self.assertNoMatchLine('# comment')

    def testBogus(self):
        self.assertNoMatchLine('bogus')

    def testSecurity(self):
        self.assertNoMatchLine('deb http://security.debian.org/debian stable main')

    def testBackports(self):
        self.assertNoMatchLine('deb http://backports.debian.org/debian stable main')

class TestErrors(TestSourcesList):
    def testFileNotFound(self):
        self.failIf(get_mirror(None, sources_list='/proc/invisible-file', defaults=None))

class TestDefaults(TestSourcesList):
    def setUp(self):
        TestSourcesList.setUp(self)
        import tempfile
        fd, self.defaults  = tempfile.mkstemp('live-magic')
        os.close(fd)

    def testDefaults(self):
        mirror = 'http://test.com/debian'
        self.f_w("bogus", self.filename)
        self.f_w("LH_MIRROR_BOOTSTRAP=\"%s\"" % mirror, self.defaults)
        ret = get_mirror(None, sources_list=self.filename, defaults=self.defaults)
        self.assertEqual(ret, mirror)

    def testDefaultsIOError(self):
        self.f_w("bogus", self.filename)
        ret = get_mirror('fallback', sources_list=self.filename, defaults='/proc/nosuchfile')
        self.assertEqual(ret, 'fallback')
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
