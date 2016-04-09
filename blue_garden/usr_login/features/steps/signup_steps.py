from behave import *
import usersdict
testuser = usersdict.testuser
testpass = usersdict.testpass

@given('a new user is at the signup page')
def step_impl(context):
    context.browser.get('http://localhost:5000/register')

    

@when('the user enters a unique username and a password')
def step_impl(context):

    form = context.browser.find_element_by_id("suform")
    usrname = context.browser.find_element_by_name('usrname')
    usrpass = context.browser.find_element_by_name('usrpass')
    usrname.send_keys(testuser)
    usrpass.send_keys(testpass)
    form.submit()
    flash = context.browser.find_element_by_id('flash')
    rv = context.client.get('/')
    assert b'log in' in rv.data
    assert 'Welcome '+testuser+'. Now you may log in!' in context.browser.page_source
    
@then('the user is registered and can login')
def step_impl(context):
    form = context.browser.find_element_by_id("suform")
    usrname = context.browser.find_element_by_name('usrname')
    usrpass = context.browser.find_element_by_name('usrpass')
    usrname.send_keys(testuser)
    usrpass.send_keys(testpass)
    form.submit()
    assert 'You were logged in' in context.browser.page_source
    
