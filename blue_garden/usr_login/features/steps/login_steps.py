from behave import *
import usersdict

testuser = usersdict.testuser
testpass = usersdict.testpass
usersdict.newuser(testuser,testpass)

@given('an existing user is at the login page')
def step_impl(context):
    context.browser.get('http://localhost:5000/login')
    
@when('the user enters a username and password which match a database entry')
def step_impl(context):
    form = context.browser.find_element_by_id("suform")
    usrname = context.browser.find_element_by_name('usrname')
    usrpass = context.browser.find_element_by_name('usrpass')
    usrname.send_keys(testuser)
    usrpass.send_keys(testpass)
    form.submit()
    

@then('the user is logged in and the users page is displayed')
def step_impl(context):
    assert 'You were logged in' in context.browser.page_source

