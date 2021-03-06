
import sqlite3
import string
from usersdict import *
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

host="localhost"
port="5000"
address="http://localhost:5000"

app = Flask(__name__)
app.config.from_object('config')

#---------------------------For selenium to automate behave tests
def serve_forever():
    app.run()#host,int(port)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with Werkzeug server")
    func()

@app.route('/shutdown')
def shutdown():
    shutdown_server()
#------------------------------------

#point to the database file defined in config.py
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('usrlist.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db() 
       
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def display_layout():
    return render_template('layout.html')

#puts user into the currently-logged-in list on database
@app.route('/add', methods=['POST'])
def add_user(uname,passw,utype):
    g.db.execute('insert into usrlist (usrname, usrpass, usrtype) values (?, ?, ?)',
                 [uname, passw, utype])
    g.db.commit()
    
    
#Adds a user to the 'users' file for subsequent authentication requests  
@app.route('/register' , methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    
    newuser(request.form['usrname'], request.form['usrpass'])
    nameof = request.form['usrname']
    flash('Welcome ' + nameof + '. Now you may log in!')
    return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    
        if authuser(request.form['usrname'], request.form['usrpass']):
            
            add_user(request.form['usrname'], request.form['usrpass'],request.form['usrtype'])                                    
            session['logged_in'] = True
            session['uid'] = request.form['usrname']
            dbcursor = g.db.execute('select sessionid from usrlist where usrname=? order by sessionid desc',
            [session['uid']])
            for entry in dbcursor:
                sessionids = [str(entry).strip(string.punctuation)] 
            sessionid = sessionids[0]
            session['sessionid'] = sessionid
            flash('You were logged in')
            if request.form['usrtype'] == 'consumer':
                return render_template('consumer.html')
            elif request.form['usrtype'] == 'producer':
                return render_template('producer.html')
            elif request.form['usrtype'] == 'distributor':
                return render_template('distributor.html')
        elif request.form['usrname'] not in usr_dict:
            error = 'Invalid username'
        elif request.form['usrpass'] not in usr_dict[request.form['usrname']]:
            error = 'Invalid password'         
    return render_template('login.html', error=error)
        
    
@app.route('/logout')
def logout():
    g.db.execute('delete from usrlist where sessionid=?',#remove the user from logged in database
    [session['sessionid']])
    g.db.commit()
    print(session['uid'],'loggedout')
    session['logged_in'] = False
    #session.clear()
    print(session)
    
    flash('You were logged out')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run()

