import unittest
from mock import Mock

from svngut.notify import Notifier

class TestNotifier(unittest.TestCase):

    def testSmoke(self):
        """Smoke test for notifier"""
        pass
        
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNotifier))
    return suite

if __name__ == '__main__':
    unittest.main()