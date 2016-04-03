
import sqlite3
from usersdict import *
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object('config')

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


@app.route('/')#note the root
def display_layout():
    
    return render_template('layout.html')

#puts user into the currently-logged-in list on database
@app.route('/add', methods=['POST'])
def add_user():
    g.db.execute('insert into usrlist (usrname, usrpass, usrtype) values (?, ?, ?)',
                 [request.form['usrname'], request.form['usrpass'], request.form['usrtype']])
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
            session['logged_in'] = True
            session['uid'] = request.form['usrname']#this should be more like:
            print(session)#id integer primary key autoincrement, because usr might clear cookies or interupt session before logout
            add_user()#and db would fail due to unique constraint
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
    g.db.execute('delete from usrlist where usrname=?',
    [session['uid']])#remove the user from logged in database
    g.db.commit()
    session.clear()
    print(session)
    
    flash('You were logged out')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run()

