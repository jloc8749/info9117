import os
from usr_login import *
import unittest
import tempfile

class usr_loginTestCase(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        if 'testname' in usr_dict:
            rm_usr('testname','testpass')
        
        
    def test_user_dict(self):
        newuser('testname','testpass')
        print('added usr')
        assert authuser('testname','testpass')
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()
