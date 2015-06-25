from flask import render_template, flash, redirect,url_for,request,session,jsonify
from dao import infoQueueDAO,videoDAO
from app import app, db_video, db_queue
from forms import LoginForm, DownloadVideoForm
import json

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

@app.route('/video', methods=['GET','POST'])
def addVideo():
    return_value = redirect(url_for('login'))
    if 'username' in session:
        form = DownloadVideoForm()
        if request.method == 'POST' and form.validate():
            db_queue.add_url(form.videoURL.data)
            return_value =  redirect('/')
        else:
            return_value =  render_template('video.html', form=form)

    return return_value

@app.route('/api/service/videos/<int:id>', methods=['GET','POST','DELETE','PUT'])
@app.route('/api/service/videos', methods=['GET','POST'])
def apiServiceVideo(id=None):
    funMap = {'GET':db_video.get_all, 'DELETE':''}
    if 'username' in session: # and request.is_xhr:
        doc_return = {}
        if request.method == 'GET':
            if id == None:
                #doc = request
                db_return = db_video.get_all()
                doc_return = {'result':db_return}
            else:
                db_return = db_video.get(id)
                doc_return = {'result':[db_return]}
        elif request.method == 'POST':
            doc = request.get_json(force=True)
            db_video.add_video(doc)
            doc_return = {'result':{'status':'ok'},}
        
        return jsonify(doc_return)
    elif True:#request.is_xhr:
        return '{}'
    else:
        return redirect(url_for('login'))
