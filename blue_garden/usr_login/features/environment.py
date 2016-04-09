from selenium import webdriver
import threading
import usr_login
import usersdict
from usr_login import app

#usr_login.app.run()

testuser = usersdict.testuser
testpass = usersdict.testpass

def before_all(ctx):
    
    ctx.server = usr_login
    ctx.address = usr_login.address
    ctx.thread = threading.Thread(target=ctx.server.serve_forever)
    ctx.thread.start()  # start flask app server
    ctx.browser = webdriver.Firefox()
    ctx.client = app.test_client()

    

def after_all(ctx):
    if usersdict.authuser(testuser,testpass):
        usersdict.rm_usr(testuser,testpass)
    ctx.browser.get(ctx.address + "/shutdown") # shut down flask app server
    ctx.thread.join()
    ctx.browser.quit()
