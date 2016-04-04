import os
import usr_login
from usr_login import *
import unittest

class usr_loginTestCase(unittest.TestCase):

    def setUp(self):
        usr_login.app.config['TESTING'] = True
        self.app = usr_login.app.test_client()
        print('setup')

    def tearDown(self):
        if 'testname' in usr_dict:
            rm_usr('testname','testpass')
        
        
    def test_user_dict(self):
        newuser('testname','testpass')
        print('added usr')
        assert authuser('testname','testpass')
        
        
        
    #def test_index_page(self):
        #rv = self.app.get('/')

        #assert 'You can either login' in rv.data
        #var1 = 'You can either login'
        #var2 = rv.data
        #self.assertEquals(var1, var2, msg=None)
        
        
        
if __name__ == '__main__':
    unittest.main()
