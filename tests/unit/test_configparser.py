import unittest
import os

from svngut.configparser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):
        path_to_config = os.path.join(os.path.dirname(__file__), 'fixtures/dummy-config.json')
        self.parser = Parser(path_to_config)

    def testGetRepositories(self):
        """Repository objects are returned correctly"""
        repos = self.parser.get_repositories()
        self.assertEqual(2, len(repos))
        for repo_key, repo in repos.items():
            self.assert_(len(repo.url) > 0)
            self.assert_(len(repo.username) > 0)
            self.assert_(len(repo.password) > 0)

    def testGetDateRange(self):
        """Date range is returned correctly"""
        range = self.parser.get_date_range()
        self.assertEqual(2, len(range))
        
    def testStartOfDateRangeIsMidnight(self):
        """Start of date range is midnight"""
        start_date = self.parser.get_date_range()[0]
        self.assertEqual(0, start_date.hour)
        self.assertEqual(0, start_date.minute)
        self.assertEqual(0, start_date.second)
        
    def testEndOfDateRangeIsOneSecondBeforeMidnight(self):
        """End of date range is one second before midnight"""
        end_date = self.parser.get_date_range()[1]
        self.assertEqual(23, end_date.hour)
        self.assertEqual(59, end_date.minute)
        self.assertEqual(59, end_date.second)
        
    def testDateRangeCoversCorrectPeriod(self):
        """Date range covers the correct period"""
        start_date = self.parser.get_date_range()[0]
        end_date = self.parser.get_date_range()[1]
        delta = end_date - start_date
        self.assertEqual(3, delta.days)
        self.assertEqual(23*60*60 + 59*60 + 59, delta.seconds)

    def testBadPathRaisesException(self):
        """Path must point to a valid file"""
        self.assertRaises(OSError, Parser, '/tmp/asdfjkl')

    def testJsonMustBeValid(self):
        """Invalid JSON raises an exception"""
        path_to_config = os.path.join(os.path.dirname(__file__), 'fixtures/invalid-config.json')
        self.assertRaises(Exception, Parser, path_to_config)

    def testGetEmailServer(self):
        """A valid email server is returned by the config parser"""
        server = self.parser.get_email_server()
        self.assert_(getattr(server, 'sendmail'))
        self.assert_(getattr(server, 'quit'))

    def testGetUserRepositories(self):
        """The user repository choices are correctly returned by the config parser"""
        user_repos = self.parser.get_user_repositories()
        self.assertEqual({'user@domain.com': ['mylibrary', 'otherlibrary']}, user_repos)
    
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestParser))
    return suite

if __name__ == '__main__':
    unittest.main()