from flask import Flask
from flask_bootstrap import Bootstrap
from tinydb  import TinyDB, where
from dao import infoQueueDAO,videoDAO

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
db_conn = TinyDB('data/youtube_dl.json')
db_queue  = infoQueueDAO(db_conn)
db_video = videoDAO(db_conn)

from app import views
