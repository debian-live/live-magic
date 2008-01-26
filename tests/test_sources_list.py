#!/usr/bin/env python

import unittest
import tempfile
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LiveMagic import models

class TestSourcesList(unittest.TestCase):
    def setUp(self):
        self.reset()

    def reset(self):
        fd, self.filename = tempfile.mkstemp('live-magic')
        os.close(fd)
        self.s = models.SourcesList(self.filename)

    def f_w(self, contents):
        f = open(self.filename, 'w+')
        f.write(contents)
        f.close()

    def testIsNotNone(self):
        self.f_w('deb http://ftp.us.debian.org/debian stable main')
        assert self.s.get_mirror() is not None

    # Match types
    def _match_type(self, url):
        self.f_w('deb %s stable main' % url)
        return self.s.get_mirror() == url

    def testDebianMirror(self):
        assert self._match_type('http://ftp.uk.debian.org/debian')

    def testLocalhost(self):
        assert self._match_type('http://localhost/debian')

    def testOtherURL(self):
        assert self._match_type('http://the.earth.li/debian')

    def testNoSecurity(self):
        assert not self._match_type('http://security.debian.org/debian')

    def testNoBackports(self):
        assert not self._match_type('http://www.backports.debian.org/debian')

    # Preferences
    def _prefer(self, ordering):
        def test():
            self.f_w("""
                deb %s stable main
                deb %s stable main
            """ % (ordering[0], ordering[1]))

            assert self.s.get_mirror() == ordering[0]

        test()
        ordering.reverse()
        self.reset()
        test()

    def testPreferLocalhost(self):
        self._prefer(['http://localhost/debian', 'http://ftp.uk.debian.org/debian'])

    def testPreferCountry(self):
        self._prefer(['http://ftp.uk.debian.org/debian', 'http://ftp.debian.org/debian'])

    def testPreferNonOfficial(self):
        self._prefer(['http://ftp.uk.debian.org/debian', 'http://backports.debian.org/debian'])

if __name__ == "__main__":
    unittest.main()
