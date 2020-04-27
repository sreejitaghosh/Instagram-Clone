import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from post import post
from followerfollowing import followerfollowing
from photocomment import photocomment

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        collection = []
        Caption = []

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

            collection_key = ndb.Key('post',user.nickname())
            collection_key = collection_key.get()
            i = 0
            if collection_key != None:
                i = len(collection_key.photo_url) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    i = i - 1
                i = len(collection_key.photo_url) - 1
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'collection' : collection,
             'Caption' : Caption,
             'i': i
        }

        template = JINJA_ENVIRONMENT.get_template('login-logout.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/photocomment',photocomment),
    ('/',MainPage),
], debug=True)
