#!/usr/bin/env python

import unittest
import tempfile
import os

import sys
sys.path.append('..')
from livemagic import model

class TestKeyVarConfigFile(unittest.TestCase):
    def setUp(self):
        fd, self.filename = tempfile.mkstemp('live-magic')
        os.close(fd)
        spec = {
            'LIVE_SPAM': 'string',
            'LIVE_MORESPAM': 'string',
            'LIVE_SPAMLIST' : 'list',
            'LIVE_SPAMBOOL' : 'boolean',
        }
        self.keyvar = model.KeyVarConfigFile(self.filename, spec)

    def f_c(self, filename=None):
        if filename is None: filename = self.filename
        return open(filename, 'r').readlines()

    def f_w(self, contents, filename=None):
        if filename is None: filename = self.filename
        f = open(filename, 'w+')
        f.write(contents)
        f.close()

    def testSetAndGetOption(self):
        self.keyvar.LIVE_SPAM = "eggs"
        assert self.keyvar.LIVE_SPAM == "eggs"

    def testSaveKnownOption(self):
        self.keyvar.LIVE_SPAM = "eggs"
        self.keyvar.save()
        assert 'LIVE_SPAM="eggs"\n' in self.f_c()

    def testSaveUnknownOption(self):
        """
        Unknown configuration keys should be added to the file.
        """
        assert len(self.f_c()) == 0
        self.keyvar.LIVE_SPAM = "eggs"
        self.keyvar.save()
        assert 'LIVE_SPAM="eggs"\n' in self.f_c()

    def testUpdatesOptions(self):
        """
        Updating an existing option should not increase the length of the file.
        """
        self.keyvar.LIVE_SPAM = "eggs"
        self.keyvar.LIVE_MORESPAM = "moreeggs"
        self.keyvar.save()
        self.keyvar.save()
        self.keyvar.load()
        save = len(self.f_c())
        self.keyvar.LIVE_SPAM = "yetmoreeggs"
        self.keyvar.save()
        assert len(self.f_c()) == save

    def testConfFileAlteredState(self):
        """
        Should change state when they have been altered.
        """
        assert self.keyvar.altered() == False
        self.keyvar.LIVE_SPAM = "eggs"
        assert self.keyvar.altered() == True

    def testConfLoadResetState(self):
        """
        Reloading the configuration should reset state.
        """
        assert self.keyvar.altered() == False
        self.keyvar.LIVE_SPAM = "eggs"
        assert self.keyvar.altered() == True
        self.keyvar.load()
        assert self.keyvar.altered() == False
        assert not hasattr(self.keyvar, 'LIVE_SPAM')

    def testSavingEscapingCharacters(self):
        """
        Characters should be escaped when saving file.
        """
        tests = {
            r'"' : r'\"',
            r'`' : r'\`',
            r'$' : r'\$',
            r'\ '[:-1] : r'\\ '[:-1],
        }
        for input, expected in tests.iteritems():
            self.keyvar.LIVE_TEST = input
            self.keyvar.save()
            self.assert_('LIVE_TEST="%s"\n' % expected in self.f_c(), \
                "Input was '%s', expected '%s'" % (input, expected))

    def testLoadingEscapedCharacters(self):
        """
        Characters should be unescaped when saving file.
        """
        tests = {
            r'Test' : r'Test',
            r'\\ '[:-1] : r'\ '[:-1],
            r'\"Test\"' : r'"Test"',
            r'\`Test\`\`Test\`' : r'`Test``Test`',
            r"\'Test\'" : r"'Test'",
        }

        for input, expected in tests.iteritems():
            # Write escaped string
            self.f_w('LIVE_SPAM="%s"' % input)

            # Reload configuration and check against expected value
            self.keyvar.load()
            self.assert_(self.keyvar.LIVE_SPAM == expected, \
                "Got back '%s', expected '%s'" % (self.keyvar.LIVE_SPAM, expected))

    def testNonStandardAlignmentAcceptance(self):
        """
        Tests acceptance of strange alignments/configurations/spacings of KEY="value" pairs.
        """
        accept = [
            r'LIVE_SPAM="eggs"',
            r'  LIVE_SPAM="eggs"  ',
            r'LIVE_SPAM="eggs" # comment # comment ',
            r'LIVE_SPAM="eggs" # comment with a " " sign',
            r'LIVE_SPAM="eggs"  ',
            r'LIVE_SPAM=eggs',
            r'LIVE_SPAM=eggs ',
            r"LIVE_SPAM='eggs' ",
        ]
        for a in accept:
            self.f_w(a)

            # Reload configuration and check against expected value
            self.keyvar.load()
            msg = "Should have accepted '%s'" % a
            try:
                self.assert_(self.keyvar.LIVE_SPAM == 'eggs', msg + ", saw '%s'" % self.keyvar.LIVE_SPAM)
            except AttributeError:
                self.fail(msg=msg)

    def testNonStandardAlignmentRejection(self):
        """
        Tests rejection strange alignments/configurations/spacings of KEY="value" pairs.
        """
        reject = [
            r'#LIVE_SPAM="eggs"', # commented out
            r'LIVE_SPAM ="eggs"',
            r'LIVE_SPAM= "eggs"',
            r'LIVE_SPAM="eggs',
            r'LIVE_SPAM=eggs"',
            r'LIVE_SPAM=spam eggs',
        ]
        for r in reject:
            self.f_w(r)

            # Reload configuration and check against expected value
            self.keyvar.load()
            self.assert_(not hasattr(self.keyvar, 'LIVE_SPAM'), "Should have rejected '%s'" % r)

    def testSaveList(self):
        expected = [
            (['eggs'], "eggs"),
            (['one', 'two', 'three'], "one two three"),
            ([' one ', ' two ', ' three '], "one two three"),
            ([], ""),
            (None, ""),
        ]

        for k, v in expected:
            self.keyvar.LIVE_SPAMLIST = k
            self.keyvar.save()
            assert 'LIVE_SPAMLIST="%s"\n' % v in self.f_c()

    def testLoadList(self):
        expected = {
            "" : [],
            "foo bar baz" : ['foo', 'bar', 'baz'],
            "foo bar-2 baz" : ['foo', 'bar-2', 'baz'],
        }

        for k, v in expected.iteritems():
            self.f_w('LIVE_SPAMLIST="%s"' % k)
            self.keyvar.load()
            assert self.keyvar.LIVE_SPAMLIST == v

    def testSaveBool(self):
        expected = {
            None : "",
            False : "disabled",
            True : "enabled",
        }

        for k, v in expected.iteritems():
            self.keyvar.LIVE_SPAMBOOL = k
            self.keyvar.save()
            assert 'LIVE_SPAMBOOL="%s"\n' % v in self.f_c()

    def testBooleanTypeLoad(self):
        expected = {
            'enabled' : True,
            'disabled' : False,
            'yes' : True,
            'no' : False,
            '' : None,
        }

        for k, v in expected.iteritems():
            self.f_w('LIVE_SPAMBOOL="%s"' % k)
            self.keyvar.load()
            assert self.keyvar.LIVE_SPAMBOOL == v

if __name__ == "__main__":
    unittest.main()
