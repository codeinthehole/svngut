import unittest

import test_svn
import test_configparser
import test_interrogator

# Register all test suites
alltests = unittest.TestSuite()
alltests.addTest(test_configparser.Suite())
alltests.addTest(test_interrogator.Suite())
alltests.addTest(test_svn.Suite())

unittest.TextTestRunner(verbosity=3).run(alltests)