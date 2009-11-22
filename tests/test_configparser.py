import unittest

from svngut.configparser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser('fixtures/dummy-config.json')

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
    
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestParser))
    return suite

if __name__ == '__main__':
    unittest.main()