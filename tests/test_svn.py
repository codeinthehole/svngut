from svngut.svn import *
from svn import UserRepositoryList

import unittest
import datetime

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repo = Repository('http://svn.example.com')

    def testUrlIsAccessible(self):
        self.assertEqual('http://svn.example.com', self.repo.url)
        
    def testCredentialsSetter(self):
        username = 'testuser'
        password = 'testpassword'
        self.repo.set_credentials(username, password)
        self.assertEqual(username, self.repo.username)
        self.assertEqual(password, self.repo.password)
        
class TestUserRepositoryList(unittest.TestCase):

    def setUp(self):
        self.email_address = 'user@domain.com'
        self.list = UserRepositoryList(self.email_address)

    def testEmailAddressIsAccessible(self):
        self.assertEqual(self.email_address, self.list.email_address)

    def testAddAndReadRepositories(self):
        self.list.add_repository(Repository('http://svn.example.com/library'))
        self.assertEqual(len(self.list.repositories), 1)

class TestCommit(unittest.TestCase):

    def setUp(self):
        self.revision = 123
        self.message = "Added some stuff"
        self.date = datetime.datetime.now()
        self.file_changes = [
            'A: /trunk/app/src/tao/classes/basket/delivery/calculator/UkStandard.php', 
            'M: /trunk/app/src/tao/classes/basket/delivery/CalculatorFactory.php', 
            'A: /trunk/app/src/tao/classes/basket/delivery/calculator', 
            'A: /trunk/app/src/tao/classes/basket/delivery/Methods.php']
        self.commit = Commit(self.revision, self.message, self.date, self.file_changes)

    def testGetNumAffectedFiles(self):
        self.assertEqual(len(self.file_changes), self.commit.get_num_affected_files())

    def testGetNumNewFiles(self):
        self.assertEqual(3, self.commit.get_num_new_files())

    def testGetNumModifiedFiles(self):
        self.assertEqual(1, self.commit.get_num_modified_files())

    def testGetNumDeletedFiles(self):
        self.assertEqual(0, self.commit.get_num_deleted_files())

def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRepository))
    suite.addTest(unittest.makeSuite(TestCommit))
    suite.addTest(unittest.makeSuite(TestUserRepositoryList))    
    return suite

if __name__ == '__main__':
    unittest.main()