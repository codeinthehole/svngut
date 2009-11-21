import unittest
import pysvn

client = pysvn.Client()

url = "http://dev.tangentlabs.co.uk/svn/riba/"
username = 'winterbottomd'
password = 'wecb132'

#def get_login( realm, username, may_save ):
#    return True, username, password, False
#
#class ClientWrapper(object):
#    
#    def __init__(self, client):
#        self._client = client
#    
#    def list(self, username, password, url):
#        print url
#        return self._client.list(url)

class TestClientApi(unittest.TestCase):

    def testFetchBranchUrls(self):
        for branch in client.ls(url):
            print branch['name']
            
            
def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClientApi))
    return suite

if __name__ == '__main__':
    unittest.main()