import os
import usr_login
import usersdict
from usr_login import *
import unittest

testuser = usersdict.testuser
testpass = usersdict.testpass

class usr_loginTestCase(unittest.TestCase):

    def setUp(self):
        usr_login.app.config['TESTING'] = True
        self.app = usr_login.app.test_client()
        print('setup')

    def tearDown(self):
        if usersdict.testuser in usr_dict:
            rm_usr(testuser,testpass)
        
#Test add user to users file        
    def test_user_dict(self):
        newuser(testuser,testpass)
        print('added usr')
        assert authuser(testuser,testpass)
        
#Test login and logged out status of cookie


#Test sqlite database for currently logged in users
        
        
#Useless test of the index page
    def test_index_page(self):
        rv = self.app.get('/')

        assert b'You can either login' in rv.data
        #var1 = 'You can either login'
        #var2 = rv.data
        #self.assertEquals(var1, var2, msg=None)
        
        
        
if __name__ == '__main__':
    unittest.main()
