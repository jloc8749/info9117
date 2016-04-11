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
        
#Test add user to users file  and login authentication passes for added user    
    def test_user_dict(self):
        #q = self.app.get('/')
        newuser(testuser,testpass)
        #self.assertEqual(q.context['text'], 'Hello!')
        assert authuser(testuser,testpass)
        #when username and password don;t match
        assert not newuser(testuser,'nottherealpassword')

#Test that existing user can login        
    def test_login(self):

        rv = self.app.post('/login',data=dict(
        usrname=testuser,
        usrpass=testpass,), follow_redirects=True)
        
        assert b'consumer' in rv.data      #'You were logged in' flash should be tested     

        
#Test login and logged out status of cookie
    def test_session(self):
        if authuser(testuser,testpass):
            rm_usr(testuser,testpass)
        
        #assert session['logged_in'] == False
        #test_user_dict()#added test user accnt and logged it in
        #logout()
        #assert self.app.session['logged_in'] == False


#Test sqlite database for currently logged in users
    def call_the_db():
        pass
        
#Useless test of the index page
    def test_index_page(self):
        rv = self.app.get('/')
        assert b'You can either login' in rv.data
        
        
        
if __name__ == '__main__':
    unittest.main()
