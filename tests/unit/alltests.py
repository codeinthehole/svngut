import unittest

import test_svn
import test_configparser
import test_interrogator
import test_digest
import test_notify

# Register all test suites
alltests = unittest.TestSuite()
alltests.addTest(test_configparser.Suite())
alltests.addTest(test_interrogator.Suite())
alltests.addTest(test_svn.Suite())
alltests.addTest(test_digest.Suite())
alltests.addTest(test_notify.Suite())

unittest.TextTestRunner(verbosity=3).run(alltests)