import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from post import post
from followerfollowing import followerfollowing
from photocomment import photocomment
from search import search
from newUsers import newUsers
from follower import follower
from following import following
from UserTimeline import UserTimeline

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
        length = 0
        userfollower = 0
        userfollowing = 0

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

            collection_key = ndb.Key('post',user.email())
            collection_key = collection_key.get()
            if collection_key != None:
                i = len(collection_key.photo_url) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    i = i - 1
                length = len(collection)
            collect = ndb.Key('followerfollowing',user.email()).get()
            if collect != None:
                userfollower = len(collect.follower)
                userfollowing = len(collect.following)
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'collection' : collection,
             'Caption' : Caption,
             'i' : length,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
        }

        template = JINJA_ENVIRONMENT.get_template('login-logout.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/',MainPage),
('/photocomment',photocomment),
('/search',search),
('/newUsers',newUsers),
('/follower',follower),
('/following',following),
('/UserTimeline',UserTimeline),
], debug=True)
