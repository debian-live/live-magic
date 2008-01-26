#!/usr/bin/env python

import unittest
import tempfile
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LiveMagic import models

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.conf = models.LiveHelperConfiguration(None)

    def testSimpleSetup(self):
        """
        Test whether we can create an empty configuration.
        """
        assert os.path.exists("%s/config/common" % self.conf.dir)

    def testFailingNewConfiguration(self):
        """Should throw IOError for an invalid directory"""
        self.assertRaises(IOError, self.conf.open, "/proc")

    def testNew(self):
        """
        new() should load a new configuration.
        """
        self.conf.common.LH_SPAM = "eggs"
        self.conf.save()
        saved_dir = self.conf.dir

        self.conf.new()
        assert not hasattr(self.conf.common, 'LH_SPAM')

        self.conf.open(saved_dir)
        assert self.conf.common.LH_SPAM == "eggs"

    def testGetOption(self):
        assert "apt" in self.conf.common.LH_APT

    def testSetKnownOption(self):
        self.conf.common.LH_APT = "apt-get"
        assert self.conf.common.LH_APT == "apt-get"

    def testSetUnknownOption(self):
        self.conf.common.LH_UNKNOWN_OPTION = "Testing value"
        assert self.conf.common.LH_UNKNOWN_OPTION == "Testing value"

    def testChildAlteredState(self):
        """
        Object should change state when a child object changes state.
        """
        assert self.conf.altered() == False
        self.conf.common.LH_SPAM = "eggs"
        assert self.conf.altered() == True

    def testConfLoadResetState(self):
        """
        Reloading the configuration should reset state.
        """
        assert self.conf.altered() == False
        self.conf.common.LH_SPAM = "eggs"
        assert self.conf.altered() == True
        self.conf.reload()
        assert not hasattr(self.conf.common, 'LH_SPAM')
        assert self.conf.altered() == False

if __name__ == "__main__":
    unittest.main()
