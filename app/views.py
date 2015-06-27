from flask import render_template, flash, redirect,url_for,request,session,jsonify
from dao import infoQueueDAO,videoDAO
from app import app, db_video, db_queue, threadList
from forms import LoginForm, DownloadVideoForm
import youtube_dl
import threading


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
        session['username'] = form.username.data
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
            return_value =  redirect('/')
            try:
                doc = db_queue.add_url(form.videoURL.data)
                newThread = threading.Thread(target=download_video_info, args=(doc,))
                threadList.append(newThread)
                newThread.start()
            except:
                print 'error in do_addURL'
        else:
            return_value =  render_template('video.html', form=form,username=session['username'])

    return return_value

@app.route('/api/service/videos/<int:id>', methods=['GET','POST','DELETE','PUT'])
@app.route('/api/service/videos', methods=['GET','POST'])
def apiServiceVideo(id=None):
    funMap = {'GET':db_video.get_all, 'DELETE':''}
    if 'username' in session and request.is_xhr:
        doc_return = {}
        if request.method == 'GET':
            if id == None:
                #doc = request
                db_return = db_video.get_all()
                doc_count = db_video.count()
                for doc in db_return: doc['_id']=doc.eid;
                doc_return = {'count':doc_count,'result':db_return}
                #print doc_return
            else:
                db_return = db_video.get(id)
                db_return['_id']=db_return.eid
                doc_return = {'result':[db_return]}
        elif request.method == 'POST':
            doc = request.get_json(force=True)
            db_video.add_video(doc)
            doc_return = {'result':{'status':'ok'},}
        elif request.method == 'DELETE':
            db_video.remove(id)
            doc_return = {'result':{'status':'ok','_id':id},}
        
        return jsonify(doc_return)
    elif request.is_xhr:
        return "{'result':{'status':'error','message':'login is required'}}"
    else:
        return redirect(url_for('login'))


@app.route('/api/service/download/<int:id>', methods=['GET'])
def apiServiceDownload(id=None):
    return_value = "{'status':'error','message':'login is required'}";
    if 'username' in session and request.is_xhr:
        doc = db_video.get(id)
        newThread = threading.Thread(target=download_video, args=(doc,))
        threadList.append(newThread)
        newThread.start()
        doc_return = {'status':'ok','message':'video will be downloaded','result':''}
        return_value = jsonify(doc_return)
    elif not(request.is_xhr):
        return_value = redirect(url_for('login'))

    return return_value


def download_video_info(video):
    if video['url'] != None:
        try:
            ydl = youtube_dl.YoutubeDL({})
            video_info = ydl.extract_info(video['url'],download=False)
            db_video.add_video(video_info)
            db_queue.remove(video.eid)
        except:
            print 'error in getting video info'

def download_progress(dl_status):
    db_video.update_dl_status(dl_status)
    if dl_status['status'] == 'downloading':
        pass
    elif dl_status['status'] == 'finished':
        pass
        #print 'video is finish'

def download_video(video):
    ydl_opts = {'progress_hooks':[download_progress]}
    if video != None:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.process_info(video)
