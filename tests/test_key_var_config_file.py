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
            'LH_SPAM': 'string',
            'LH_MORESPAM': 'string',
            'LH_SPAMLIST' : 'list',
            'LH_SPAMBOOL' : 'boolean',
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
        self.keyvar.LH_SPAM = "eggs"
        assert self.keyvar.LH_SPAM == "eggs"

    def testSaveKnownOption(self):
        self.keyvar.LH_SPAM = "eggs"
        self.keyvar.save()
        assert 'LH_SPAM="eggs"\n' in self.f_c()

    def testSaveUnknownOption(self):
        """
        Unknown configuration keys should be added to the file.
        """
        assert len(self.f_c()) == 0
        self.keyvar.LH_SPAM = "eggs"
        self.keyvar.save()
        assert 'LH_SPAM="eggs"\n' in self.f_c()

    def testUpdatesOptions(self):
        """
        Updating an existing option should not increase the length of the file.
        """
        self.keyvar.LH_SPAM = "eggs"
        self.keyvar.LH_MORESPAM = "moreeggs"
        self.keyvar.save()
        self.keyvar.save()
        self.keyvar.load()
        save = len(self.f_c())
        self.keyvar.LH_SPAM = "yetmoreeggs"
        self.keyvar.save()
        assert len(self.f_c()) == save

    def testConfFileAlteredState(self):
        """
        Should change state when they have been altered.
        """
        assert self.keyvar.altered() == False
        self.keyvar.LH_SPAM = "eggs"
        assert self.keyvar.altered() == True

    def testConfLoadResetState(self):
        """
        Reloading the configuration should reset state.
        """
        assert self.keyvar.altered() == False
        self.keyvar.LH_SPAM = "eggs"
        assert self.keyvar.altered() == True
        self.keyvar.load()
        assert self.keyvar.altered() == False
        assert not hasattr(self.keyvar, 'LH_SPAM')

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
            self.keyvar.LH_TEST = input
            self.keyvar.save()
            self.assert_('LH_TEST="%s"\n' % expected in self.f_c(), \
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
            self.f_w('LH_SPAM="%s"' % input)

            # Reload configuration and check against expected value
            self.keyvar.load()
            self.assert_(self.keyvar.LH_SPAM == expected, \
                "Got back '%s', expected '%s'" % (self.keyvar.LH_SPAM, expected))

    def testNonStandardAlignmentAcceptance(self):
        """
        Tests acceptance of strange alignments/configurations/spacings of KEY="value" pairs.
        """
        accept = [
            r'LH_SPAM="eggs"',
            r'  LH_SPAM="eggs"  ',
            r'LH_SPAM="eggs" # comment # comment ',
            r'LH_SPAM="eggs" # comment with a " " sign',
            r'LH_SPAM="eggs"  ',
            r'LH_SPAM=eggs',
            r'LH_SPAM=eggs ',
            r"LH_SPAM='eggs' ",
        ]
        for a in accept:
            self.f_w(a)

            # Reload configuration and check against expected value
            self.keyvar.load()
            msg = "Should have accepted '%s'" % a
            try:
                self.assert_(self.keyvar.LH_SPAM == 'eggs', msg + ", saw '%s'" % self.keyvar.LH_SPAM)
            except AttributeError:
                self.fail(msg=msg)

    def testNonStandardAlignmentRejection(self):
        """
        Tests rejection strange alignments/configurations/spacings of KEY="value" pairs.
        """
        reject = [
            r'#LH_SPAM="eggs"', # commented out
            r'LH_SPAM ="eggs"',
            r'LH_SPAM= "eggs"',
            r'LH_SPAM="eggs',
            r'LH_SPAM=eggs"',
            r'LH_SPAM=spam eggs',
        ]
        for r in reject:
            self.f_w(r)

            # Reload configuration and check against expected value
            self.keyvar.load()
            self.assert_(not hasattr(self.keyvar, 'LH_SPAM'), "Should have rejected '%s'" % r)

    def testSaveList(self):
        expected = [
            (['eggs'], "eggs"),
            (['one', 'two', 'three'], "one two three"),
            ([' one ', ' two ', ' three '], "one two three"),
            ([], ""),
            (None, ""),
        ]

        for k, v in expected:
            self.keyvar.LH_SPAMLIST = k
            self.keyvar.save()
            assert 'LH_SPAMLIST="%s"\n' % v in self.f_c()

    def testLoadList(self):
        expected = {
            "" : [],
            "foo bar baz" : ['foo', 'bar', 'baz'],
            "foo bar-2 baz" : ['foo', 'bar-2', 'baz'],
        }

        for k, v in expected.iteritems():
            self.f_w('LH_SPAMLIST="%s"' % k)
            self.keyvar.load()
            assert self.keyvar.LH_SPAMLIST == v

    def testSaveBool(self):
        expected = {
            None : "",
            False : "disabled",
            True : "enabled",
        }

        for k, v in expected.iteritems():
            self.keyvar.LH_SPAMBOOL = k
            self.keyvar.save()
            assert 'LH_SPAMBOOL="%s"\n' % v in self.f_c()

    def testBooleanTypeLoad(self):
        expected = {
            'enabled' : True,
            'disabled' : False,
            'yes' : True,
            'no' : False,
            '' : None,
        }

        for k, v in expected.iteritems():
            self.f_w('LH_SPAMBOOL="%s"' % k)
            self.keyvar.load()
            assert self.keyvar.LH_SPAMBOOL == v

if __name__ == "__main__":
    unittest.main()
