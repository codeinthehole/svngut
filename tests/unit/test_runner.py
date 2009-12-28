import svngut.runner
import unittest
import datetime

class TestGetUserRepositories(unittest.TestCase):

    def testUrlIsAccessible(self):
        self.assertEqual('http://svn.example.com', self.repo.url)
        
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRepository))
    return suite

if __name__ == '__main__':
    unittest.main()