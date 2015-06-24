from flask import render_template, flash, redirect,url_for,request,session
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html',username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        session['username'] = form.username
        return redirect('/')
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for('login'))
