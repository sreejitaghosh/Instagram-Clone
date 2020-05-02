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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class follower(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url_string = ''
        url = ''
        userfollower = 0
        userfollowing = 0
        newfollower = ""
        user = users.get_current_user()
        if user:
            email = self.request.get('email_address')
            if email == "":
                email = user.email()
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_details = ndb.Key('MyUser',user.email())
            myuser = myuser_details.get()
            if myuser == None:
                myuser = MyUser(id=user.email())
                myuser.email_address = user.email()
                myuser.userId = user.nickname()
                welcome = 'Welcome to the application'
                myuser.put()
            collect = ndb.Key('followerfollowing',email).get()
            if collect != None:
                if collect.following != None:
                    newfollower = collect.follower
                else:
                    newfollower = []
            else:
                newfollower = []
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'newfollower': newfollower,
        }

        template = JINJA_ENVIRONMENT.get_template('follower.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/follower',follower),
], debug=True)
