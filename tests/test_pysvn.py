import unittest
import pysvn

client = pysvn.Client()

url = "http://dev.tangentlabs.co.uk/svn/riba/"
username = 'winterbottomd'
password = 'wecb132'

def get_login( realm, username, may_save ):
    return True, username, password, False

class ClientWrapper(object):
    
    def __init__(self, client):
        self._client = client
    
    def list(self, username, password, url):
        print url
        return self._client.list(url)

#client.callback_get_login = get_login
client = pysvn.Client()
wrapper = ClientWrapper(client)

print wrapper.list(username, password, url)