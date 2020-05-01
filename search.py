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

class search(webapp2.RequestHandler):
    def get(self):
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
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        Raw_Data = MyUser.query()
        Search_KeyWord = self.request.get('search')
        Result = []
        Found = Raw_Data.filter(MyUser.email_address == Search_KeyWord).fetch()
        if Found == []:
            Found = Raw_Data.filter(MyUser.userId == Search_KeyWord).fetch()
            if Found == []:
                Raw_Data = Raw_Data.fetch()
                for i in range(0,len(Raw_Data)):
                    if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
                    elif Raw_Data[i].userId.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
            else:
                Result.append(Found[0].email_address)
        else:
            Result.append(Found[0].email_address)

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'Result' : Result,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
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
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        Raw_Data = MyUser.query()
        Search_KeyWord = self.request.get('search')
        Result = []
        Found = Raw_Data.filter(MyUser.email_address == Search_KeyWord).fetch()
        if Found == []:
            Found = Raw_Data.filter(MyUser.userId == Search_KeyWord).fetch()
            if Found == []:
                Raw_Data = Raw_Data.fetch()
                for i in range(0,len(Raw_Data)):
                    if Raw_Data[i].email_address.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
                    elif Raw_Data[i].userId.find(Search_KeyWord) != -1:
                        Result.append(Raw_Data[i].email_address)
            else:
                Result.append(Found[0].email_address)
        else:
            Result.append(Found[0].email_address)

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'Result' : Result,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/search',search),
], debug=True)
