#!/usr/bin/env python

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianLive.elements import KeyVar

class TestKeyVar(unittest.TestCase):
    spec = {
        'LH_SPAM': str,
        'LH_MORE_SPAM': str,
        'LH_SPAM_LIST' : list,
        'LH_SPAM_BOOL' : bool,
    }

    initial = """
 LH_SPAM="eggs"
 LH_MORE_SPAM="more eggs"
   LH_SPAM_LIST="spam eggs ham bacon"
        LH_SPAM_BOOL="disabled"
    """

    name = 'test_key_var'

    def setUp(self, reset=False):
        import tempfile
        self.dir = tempfile.mkdtemp('debian-live')
        os.makedirs(os.path.join(self.dir, 'config'))

        self.filename = os.path.join(self.dir, 'config', self.name)
        f = open(self.filename, 'w+')
        f.write(self.initial)
        f.close()

        self.key_var = KeyVar(self.dir, self.name, self.spec)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir)

    def reset(self):
        self.tearDown()
        self.setUp()

    def f_c(self, filename=None):
        if filename is None:
            filename = self.filename
        return [x.strip() for x in open(filename, 'r').readlines()]

    ###

class TestSimple(TestKeyVar):
    def testSetAndGetOption(self):
        self.key_var['LH_SPAM'] = 'eggs'
        self.assertEqual(self.key_var['LH_SPAM'], 'eggs')

    def testSaveKnownOption(self):
        self.key_var['LH_SPAM'] = "eggs"
        assert 'LH_SPAM="eggs"' in self.f_c()

    def testSaveUnknownOption(self):
        """
        Unknown configuration keys should be added to the file.
        """
        self.key_var['LH_UNKNOWN_OPTION'] = 'spam'
        self.key_var.save()
        assert 'LH_UNKNOWN_OPTION="spam"' in self.f_c()

class TestSaveEscaped(TestKeyVar):
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
            self.key_var['LH_TEST'] = input
            self.key_var.save()
            self.assert_('LH_TEST="%s"' % expected in self.f_c(), \
                "Input was '%s', expected '%s'" % (input, expected))

class TestLoadEscaped(TestKeyVar):
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
            self.initial = 'LH_SPAM="%s"' % input

            # Reload configuration and check against expected value
            self.reset()
            self.assert_(self.key_var['LH_SPAM'] == expected, \
                "Got back '%s', expected '%s'" % (self.key_var['LH_SPAM'], expected))

class TestAccept(TestKeyVar):
    """
    Tests acceptance of strange alignments/configurations/spacings of KEY="value" pairs.
    """

    def assertAccepts(self, input):
        self.initial = input
        self.reset()
        self.assertEquals(self.key_var['LH_SPAM'], 'eggs')

    def testNormal(self):
        self.assertAccepts(r'LH_SPAM="eggs"')

    def testSpacing(self):
        self.assertAccepts(r"LH_SPAM='eggs' ")

    def testSpacingBoth(self):
        self.assertAccepts(r'  LH_SPAM="eggs"  ')

    def testTwoComments(self):
        self.assertAccepts(r'LH_SPAM="eggs" # comment # comment ')

    def testCommentsWithQuotes(self):
        self.assertAccepts(r'LH_SPAM="eggs" # comment with a " " sign')

    def testSpacingEnd(self):
        self.assertAccepts(r'LH_SPAM="eggs"  ')

    def testNoQuotes(self):
        self.assertAccepts(r'LH_SPAM=eggs')

    def testNoQuotesSpacing(self):
        self.assertAccepts(r'LH_SPAM=eggs ')

class TestAllignmentReject(TestKeyVar):
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
            self.initial = r
            self.reset()
            self.assertEqual(repr(self.key_var), '{}')

class TestSaveLists(TestKeyVar):
    def testSaveList(self):
        expected = [
            (['eggs'], "eggs"),
            (['one', 'two', 'three'], "one two three"),
            ([' one ', ' two ', ' three '], "one two three"),
            ([], ""),
            (None, ""),
        ]

        for k, v in expected:
            self.key_var['LH_SPAM_LIST'] = k
            self.key_var.save()
            assert 'LH_SPAM_LIST="%s"' % v in self.f_c()


class TestLoadLists(TestKeyVar):
    def assertLoadsAs(self, input, expected):
        self.initial = 'LH_SPAM_LIST="%s"' % input
        self.reset()
        self.assertEqual(self.key_var['LH_SPAM_LIST'], expected)

    def testEmptyString(self):
        self.assertLoadsAs("", [])

    def testSimpleList(self):
        self.assertLoadsAs('foo bar baz', ['foo', 'bar', 'baz'])

    def testSimpleListTwo(self):
        self.assertLoadsAs('foo bar-2 baz', ['foo', 'bar-2', 'baz'])

class TestBoolSave(TestKeyVar):
    def assertSavesAs(self, input, expected):
        self.key_var['LH_SPAMBOOL'] = input
        self.key_var.save()
        assert 'LH_SPAMBOOL="%s"' % expected in self.f_c()

    def testSaveNone(self):
        self.assertSavesAs(None, '')

    def testSaveFalse(self):
        self.assertSavesAs(False, 'disabled')

    def testSaveTrue(self):
        self.assertSavesAs(True, 'enabled')

class TestBoolLoad(TestKeyVar):
    def assertParsesAs(self, input, expected):
        self.initial = 'LH_SPAM_BOOL="%s"' % input
        self.reset()
        self.assertEqual(self.key_var['LH_SPAM_BOOL'], expected)

    def testEnabled(self):
        self.assertParsesAs('enabled', True)

    def testDisabled(self):
        self.assertParsesAs('disabled', False)

    def testYes(self):
        self.assertParsesAs('yes', True)

    def testNo(self):
        self.assertParsesAs('no', False)

    def testBlank(self):
        self.assertParsesAs('', None)
        self.assertParsesAs(' ', None)

if __name__ == "__main__":
    unittest.main()
