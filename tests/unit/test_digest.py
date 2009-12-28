import unittest
from mock import Mock

from svngut.digest import Summariser

class TestSummariser(unittest.TestCase):

    def testSnoke(self):
        """Smoke test for summariser"""
        pass
        
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSummariser))
    return suite

if __name__ == '__main__':
    unittest.main()