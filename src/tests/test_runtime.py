from svngut.runtime import *
import unittest
import datetime

class TestSvnCommit(unittest.TestCase):

    def setUp(self):
        self.revision = 123
        self.message = "Added some stuff"
        self.date = datetime.datetime.now()
        self.file_changes = [
            'A: /trunk/app/src/tao/classes/basket/delivery/calculator/UkStandard.php', 
            'M: /trunk/app/src/tao/classes/basket/delivery/CalculatorFactory.php', 
            'A: /trunk/app/src/tao/classes/basket/delivery/calculator', 
            'A: /trunk/app/src/tao/classes/basket/delivery/Methods.php']
        self.commit = SvnCommit(self.revision, self.message, self.date, self.file_changes)

    def testGetNumAffectedFiles(self):
        self.assertEqual(len(self.file_changes), self.commit.get_num_affected_files())

    def testGetNumNewFiles(self):
        self.assertEqual(3, self.commit.get_num_new_files())

    def testGetNumModifiedFiles(self):
        self.assertEqual(1, self.commit.get_num_modified_files())

    def testGetNumDeletedFiles(self):
        self.assertEqual(0, self.commit.get_num_deleted_files())

if __name__ == '__main__':
    unittest.main()