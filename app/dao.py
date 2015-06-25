from tinydb import TinyDB,where


class videoDAO:

    def __init__(self, db):
        self.db = db
        self.video = db.table('video')


    def add_video(self,video):
        try:
            video.pop('formats',None)
            eid = self.video.insert(video)
        except:
            print 'error in insert video'

    def remove(self,eid):
        try:
            self.video.remove(eids = [eid])
        except:
            print 'error in removing video'

    def get(self,eid):
        doc = None
        try:
            doc = self.video.get(eid=eid)
        except:
            print "error in getteing video"

        return doc

    def get_all(self):
        urls = []
        try:
            urls = self.video.all()
        except:
            print 'error in geting all video'

        return urls

    def update_dl_status(self,dl_status):
        youtube_id = self._parse_youtubeID(dl_status['filename'])
        doc = self.video.get(where('id') == youtube_id)
        self.video.update({'dl_status':dl_status}, eids=[doc.eid])

    def _parse_youtubeID(self,fileName):
        youtube_id = fileName.split('.')[-2][-11:]
        return youtube_id


class infoQueueDAO:

    def __init__(self, db):
        self.db = db
        self.info_queue = db.table('info_queue')


    def add_url(self,url):
        video_id = self._parseURL(url)
        tmpUrl = {'url':url,'video_id':video_id}
        try:
            eid = self.info_queue.insert(tmpUrl)
            doc = self.info_queue.get(eid=eid)
            return doc
        except:
            print 'error in insert url'

    def remove(self,eid):
        try:
            self.info_queue.remove(eids=[eid])
        except:
            print 'error in removing video'

    def get_all(self):
        urls = []
        try:
            urls = self.info_queue.all()
        except:
            print 'error in geting all url'

        return urls

    def _parseURL(self,url):
        video_id = None
        base_url,url_parameter = url.split('?')
        url_params = url_parameter.split('&')
        for param in url_params:
            param_name, param_value = param.split('=')
            if param_name == 'v':
                video_id = param_value

        return video_id


class urlDAO:

    def __init__(self, db):
        self.db = db
        self.url = db.table('info_queue')


    def add_url(self,url):
        video_id = self._parseURL(url)
        tmpUrl = {'url':url,'video_id':video_id}
        try:
            eid = self.url.insert(tmpUrl)
        except:
            print 'error in insert url'

    def get_all(self):
        urls = []
        try:
            urls = self.url.all()
        except:
            print 'error in geting all url'

        return urls

    def _parseURL(self,url):
        video_id = None
        base_url,url_parameter = url.split('?')
        url_params = url_parameter.split('&')
        for param in url_params:
            param_name, param_value = param.split('=')
            if param_name == 'v':
                video_id = param_value

        return video_id
