import unittest
from mock import Mock

from svngut.svn import Repository
from svngut.interrogator import RepositoryInterrogator
import datetime

svn_base_url = 'http://svn.example.com/project/'

def returnDummyUrls(base_url):
    if base_url == svn_base_url:
        return getDummySvnDirs(('trunk/', 'branches/')) 
    elif base_url == '%sbranches/' % svn_base_url:
        return getDummySvnDirs(('branches/dev/',))
    raise ValueError("Unrecognised argument: %s" % base_url)

def returnDummySvnDirs(url):
    return getDummySvnDirs(('trunk/', 'tags/', 'branches/'))

def getDummySvnDirs(paths):
    dirs = []
    for url_path in paths:
        svn_dir = {'name': '%s%s' % (svn_base_url, url_path)}
        dirs.append(svn_dir)
    return dirs

class TestInterrogator(unittest.TestCase):

    def getDummyRepository(self):
        return Repository(svn_base_url) 

    def getDummyDateRange(self):
        today = datetime.date.today()
        start_date = datetime.datetime(today.year, today.month, today.day-3, 0, 0, 0)
        end_date = datetime.datetime(today.year, today.month, today.day-1, 23, 59, 59)
        return (start_date, end_date)

    def testGetUrlList(self):
        client = Mock()
        client.ls = Mock()
        client.ls.side_effect = returnDummySvnDirs
        
        interrogator = RepositoryInterrogator(client)
        urls = interrogator.get_url_list(svn_base_url)
        expected_urls = ['http://svn.example.com/project/trunk/', 
                         'http://svn.example.com/project/branches/',
                         'http://svn.example.com/project/tags/']
        urls.sort()
        expected_urls.sort()
        self.assertEqual(expected_urls, urls)
        
    def testGetBranchUrls(self):
        client = Mock()
        client.ls = Mock()
        client.ls.side_effect = returnDummyUrls
        
        interrogator = RepositoryInterrogator(client)
        urls = interrogator.get_branch_urls(self.getDummyRepository())
        expected_urls = ['http://svn.example.com/project/trunk/', 
                         'http://svn.example.com/project/branches/dev/']
        urls.sort()
        expected_urls.sort()
        self.assertEquals(expected_urls, urls)
        
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInterrogator))
    return suite

if __name__ == '__main__':
    unittest.main()