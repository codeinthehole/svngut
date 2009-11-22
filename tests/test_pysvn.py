import unittest
import pysvn
import time
import datetime
import pprint

client = pysvn.Client()

url = "http://dev.tangentlabs.co.uk/svn/riba/"
username = 'winterbottomd'
password = 'wecb132'

class TestClientApi(unittest.TestCase):

    def testFetchBranchUrls(self):
        for branch in client.ls(url):
            print branch['name']
    
    def getDummyDateRange(self):
        today = datetime.date.today()
        start_date = datetime.datetime(today.year, today.month, today.day-3, 0, 0, 0)
        end_date = datetime.datetime(today.year, today.month, today.day-1, 23, 59, 59)
        return (start_date, end_date)
    
    def testFetchCommits(self):
        date_range = self.getDummyDateRange()
        start_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[0].timetuple()))
        end_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[1].timetuple()))
        raw_commits = client.log(url, 
                                 revision_start=start_revision, 
                                 revision_end=end_revision,
                                 discover_changed_paths=True)
        for commit in raw_commits:
            pprint.pprint(commit.items())
            for change in commit.changed_paths:
                 pprint.pprint(change.items())
            
            
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClientApi))
    return suite

if __name__ == '__main__':
    unittest.main()