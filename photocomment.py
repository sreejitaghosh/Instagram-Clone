import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import os
from user import MyUser
from post import post
from followerfollowing import followerfollowing
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class photocomment(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url_string = ''
        url = ''
        collection_key = []
        user = users.get_current_user()
        upload_url = ""

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser', user.email())
            myuser = myuser_details.get()
            upload_url = blobstore.create_upload_url('/photocomment')
            if myuser == None:
                myuser = MyUser(id=user.email())
                myuser.email_address = user.email()
                myuser.userId = user.nickname()
                welcome = 'Welcome to the application'
                myuser.put()

            collection_key = ndb.Key('post', user.email())
            collection_key = collection_key.get()
            if collection_key == None:
                collection_key = post(id=user.email())
                collection_key.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'collection_key' : collection_key,
             'upload_url' : upload_url,
        }

        template = JINJA_ENVIRONMENT.get_template('photocomment.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser', user.email())
            myuser = myuser_details.get()
            if myuser == None:
                myuser = MyUser(id=user.email())
                myuser.email_address = user.email()
                myuser.userId = user.nickname()
                welcome = 'Welcome to the application'
                myuser.put()

            upload = self.get_uploads()[0]
            blobinfo = blobstore.BlobInfo(upload.key())
            image_url = get_serving_url(blobinfo)
            caption = self.request.get('caption')
            collection_key = ndb.Key('post',user.email())
            collection_key = collection_key.get()

            if collection_key == None:
                collection_key = post(id = user.email())
                collection_key.photo_url.append(image_url)
                collection_key.email_address = user.email()
                collection_key.caption.append(caption)
            else:
                collection_key.photo_url.append(image_url)
                collection_key.email_address = user.email()
                collection_key.caption.append(caption)

            collection_key.put()
            self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'collection_key' : collection_key,
        }

        template = JINJA_ENVIRONMENT.get_template('photocomment.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/photocomment',photocomment),
], debug=True)
