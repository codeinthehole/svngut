import unittest
import datetime

from svngut.svn import *

class TestRepository(unittest.TestCase):
    """Testing repository object"""

    def setUp(self):
        self.repo = Repository('http://svn.example.com')

    def testUrlIsAccessible(self):
        """Url property is accessible"""
        self.assertEqual('http://svn.example.com', self.repo.url)
        
    def testCredentialsSetter(self):
        """Repository credentials can be set"""
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
        """Email address is publicly available"""
        self.assertEqual(self.email_address, self.list.email_address)

    def testAddAndReadRepositories(self):
        """Repositories can be added and then read"""
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
        """Number of affected files is correct"""
        self.assertEqual(len(self.file_changes), self.commit.get_num_affected_files())

    def testGetNumNewFiles(self):
        """Number of new files is correct"""
        self.assertEqual(3, self.commit.get_num_new_files())

    def testGetNumModifiedFiles(self):
        """Number of modified files is correct"""
        self.assertEqual(1, self.commit.get_num_modified_files())

    def testGetNumDeletedFiles(self):
        """Number of deleted files is correct"""
        self.assertEqual(0, self.commit.get_num_deleted_files())

class TestBranchContribution(unittest.TestCase):
    
    def testUsernameIsAccessible(self):
        """Username is publicly accessible"""
        contribution = BranchContribution('barry', 'http://svn.example.com/project/branches/dev/', [])
        self.assertEqual('barry', contribution.username)

    

def Suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRepository))
    suite.addTest(unittest.makeSuite(TestCommit))
    suite.addTest(unittest.makeSuite(TestUserRepositoryList))
    suite.addTest(unittest.makeSuite(TestBranchContribution))       
    return suite

if __name__ == '__main__':
    unittest.main()