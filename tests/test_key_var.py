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

from DebianLive.elements import KeyVar

class TestKeyVar(unittest.TestCase):
    spec = {
        'LB_SPAM': str,
        'LB_MORE_SPAM': str,
        'LB_SPAM_LIST' : list,
        'LB_SPAM_BOOL' : bool,
    }

    initial = """
        LB_SPAM="eggs"
        LB_MORE_SPAM="more eggs"
        LB_SPAM_LIST="spam eggs ham bacon"
        LB_SPAM_BOOL="false"
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
        self.key_var['LB_SPAM'] = 'eggs'
        self.assertEqual(self.key_var['LB_SPAM'], 'eggs')

    def testSetAndGetOptionSpecifyFilename(self):
        self.key_var = KeyVar('/', 'dummy', self.spec, filename=self.filename)
        self.key_var['LB_SPAM'] = 'eggs'
        self.assertEqual(self.key_var['LB_SPAM'], 'eggs')

    def testSaveKnownOption(self):
        self.key_var['LB_SPAM'] = 'new value'
        self.key_var.save()
        self.assert_('LB_SPAM="new value"' in self.f_c())

    def testSaveKnownOptionNoChange(self):
        before = self.f_c()
        self.key_var['LB_SPAM'] = 'eggs'
        self.key_var.save()
        self.assertEqual(before, self.f_c())

    def testSaveUnknownOption(self):
        """
        Unknown configuration keys should be added to the file.
        """
        self.key_var['LB_UNKNOWN_OPTION'] = 'spam'
        self.key_var.save()
        self.assert_('LB_UNKNOWN_OPTION="spam"' in self.f_c())

    def testSaveUnknownOptionNewSize(self):
        len_before = len(self.f_c())
        self.key_var['LB_UKNOWN_OPTION'] = 'new value'
        self.key_var.save()
        self.assert_(len(self.f_c()) > len_before)

    def testSaveNoChanges(self):
        self.key_var.save()

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
            self.key_var['LB_TEST'] = input
            self.key_var.save()
            self.assert_('LB_TEST="%s"' % expected in self.f_c(), \
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
            self.initial = 'LB_SPAM="%s"' % input

            # Reload configuration and check against expected value
            self.reset()
            self.assert_(self.key_var['LB_SPAM'] == expected, \
                "Got back '%s', expected '%s'" % (self.key_var['LB_SPAM'], expected))

class TestAccept(TestKeyVar):
    """
    Tests acceptance of strange alignments/configurations/spacings of KEY="value" pairs.
    """

    def assertAccepts(self, input):
        self.initial = input
        self.reset()
        self.assertEquals(self.key_var['LB_SPAM'], 'eggs')

    def testNormal(self):
        self.assertAccepts(r'LB_SPAM="eggs"')

    def testSpacing(self):
        self.assertAccepts(r"LB_SPAM='eggs' ")

    def testSpacingBoth(self):
        self.assertAccepts(r'  LB_SPAM="eggs"  ')

    def testTwoComments(self):
        self.assertAccepts(r'LB_SPAM="eggs" # comment # comment ')

    def testCommentsWithQuotes(self):
        self.assertAccepts(r'LB_SPAM="eggs" # comment with a " " sign')

    def testSpacingEnd(self):
        self.assertAccepts(r'LB_SPAM="eggs"  ')

    def testNoQuotes(self):
        self.assertAccepts(r'LB_SPAM=eggs')

    def testNoQuotesSpacing(self):
        self.assertAccepts(r'LB_SPAM=eggs ')

class TestAllignmentReject(TestKeyVar):
    def testNonStandardAlignmentRejection(self):
        """
        Tests rejection strange alignments/configurations/spacings of KEY="value" pairs.
        """
        reject = [
            r'#LB_SPAM="eggs"', # commented out
            r'LB_SPAM ="eggs"',
            r'LB_SPAM= "eggs"',
            r'LB_SPAM="eggs',
            r'LB_SPAM=eggs"',
            r'LB_SPAM=spam eggs',
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
            self.key_var['LB_SPAM_LIST'] = k
            self.key_var.save()
            assert 'LB_SPAM_LIST="%s"' % v in self.f_c()


class TestLists(TestKeyVar):
    def testAppend(self):
        self.key_var['LB_SPAM_LIST'].append('ketchup')
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testSetItem(self):
        self.key_var['LB_SPAM_LIST'][0] = 'ketchup'
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testDelItem(self):
        del self.key_var['LB_SPAM_LIST'][0]
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testSetSlice(self):
        self.key_var['LB_SPAM_LIST'][:] = []
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testDelSlice(self):
        del self.key_var['LB_SPAM_LIST'][:]
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testPop(self):
        self.key_var['LB_SPAM_LIST'].pop()
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testExtend(self):
        self.key_var['LB_SPAM_LIST'].extend(range(3))
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testInsert(self):
        self.key_var['LB_SPAM_LIST'].insert(0, 'spam')
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testRemove(self):
        self.key_var['LB_SPAM_LIST'].remove('spam')
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testReverse(self):
        self.key_var['LB_SPAM_LIST'].reverse()
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testSort(self):
        self.key_var['LB_SPAM_LIST'].sort()
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

    def testSetList(self):
        self.key_var['LB_SPAM_LIST'] = ['spam']
        self.key_var.save()
        self.key_var['LB_SPAM_LIST'].append('ketchup')
        self.assert_('LB_SPAM_LIST' in self.key_var.stale)

class TestLoadLists(TestKeyVar):
    def assertLoadsAs(self, input, expected):
        self.initial = 'LB_SPAM_LIST="%s"' % input
        self.reset()
        self.assertEqual(self.key_var['LB_SPAM_LIST'], expected)

    def testEmptyString(self):
        self.assertLoadsAs("", [])

    def testSimpleList(self):
        self.assertLoadsAs('foo bar baz', ['foo', 'bar', 'baz'])

    def testSimpleListTwo(self):
        self.assertLoadsAs('foo bar-2 baz', ['foo', 'bar-2', 'baz'])

class TestBoolSave(TestKeyVar):
    def assertSavesAs(self, input, expected):
        self.key_var['LB_SPAMBOOL'] = input
        self.key_var.save()
        assert 'LB_SPAMBOOL="%s"' % expected in self.f_c()

    def testSaveNone(self):
        self.assertSavesAs(None, '')

    def testSaveFalse(self):
        self.assertSavesAs(False, 'false')

    def testSaveTrue(self):
        self.assertSavesAs(True, 'true')

class TestBoolLoad(TestKeyVar):
    def assertParsesAs(self, input, expected):
        self.initial = 'LB_SPAM_BOOL="%s"' % input
        self.reset()
        self.assertEqual(self.key_var['LB_SPAM_BOOL'], expected)

    def testEnabled(self):
        self.assertParsesAs('true', True)

    def testDisabled(self):
        self.assertParsesAs('false', False)

    def testYes(self):
        self.assertParsesAs('yes', True)

    def testNo(self):
        self.assertParsesAs('no', False)

    def testBlank(self):
        self.assertParsesAs('', None)
        self.assertParsesAs(' ', None)

if __name__ == "__main__":
    unittest.main()
