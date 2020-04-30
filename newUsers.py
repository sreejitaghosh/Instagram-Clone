import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from post import post
from followerfollowing import followerfollowing
from photocomment import photocomment
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class newUsers(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url_string = ''
        url = ''
        collection = []
        Caption = []
        userfollower = 0
        userfollowing = 0

        user = users.get_current_user()
        followDecission = ""
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

            newEmail = self.request.get('email_address')
            newUsers = ndb.Key('MyUser',newEmail).get()
            collection_key = ndb.Key('post',newUsers.userId)
            collection_key = collection_key.get()
            newUserFFList = ndb.Key('followerfollowing',newEmail).get()
            if collection_key != None:
                i = len(collection_key.photo_url) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    i = i - 1
                length = len(collection)

            newUsersId =  newUsers.userId
            collect = ndb.Key('followerfollowing',newUsersId).get()
            if collect != None:
                userfollower = len(collect.follower)
                userfollowing = len(collect.following)
                for i in collect.follower:
                    if i == user.email():
                        followDecission = 'True'
                        break
                    else:
                        followDecission = 'False'
            else:
                userfollower = 0
                userfollowing = 0
                followDecission = 'False'
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
             'newUsers' : newUsers,
             'newEmail' : newEmail,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'followDecission' : followDecission,
        }
        template = JINJA_ENVIRONMENT.get_template('newUsers.html')
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


        new_Email = self.request.get('email_address')
        new_Users = ndb.Key('MyUser',new_Email).get()
        newUsers_Id = new_Users.userId
        collect_ff_new = ndb.Key('followerfollowing',newUsers_Id).get()

        old_Email = user.email()
        old_Users = ndb.Key('MyUser',old_Email).get()
        oldUsers_Id = old_Users.userId
        collect_ff_old = ndb.Key('followerfollowing',oldUsers_Id).get()

        button = self.request.get('submit')
        if button == 'Follow':
            if collect_ff_old != None:
                collect_ff_old.following.append(new_Email)
                collect_ff_old.put()
            else:
                collect_ff_old = followerfollowing(id=oldUsers_Id)
                collect_ff_old.following.append(new_Email)
                collect_ff_old.put()

            if collect_ff_new != None:
                collect_ff_new.follower.append(user.email())
                collect_ff_new.put()
            else:
                collect_ff_new = followerfollowing(id=newUsers_Id)
                collect_ff_new.follower.append(user.email())
                collect_ff_new.put()

        elif button == 'Unfollow':
            for i in range(0,len(collect_ff_old.following)):
                if collect_ff_old.following[i] == collect_ff_new:
                    del collect_ff_old.following[i]
                    collect_ff_old.put()
                    break

            for l in range(0,len(collect_ff_new.follower)):
                if collect_ff_new.follower[l] == collect_ff_old.userId:
                    del collect_ff_new.follower[l]
                    collect_ff_new.put()
                    break



        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'new_Users' : new_Users,
             'new_Email' : new_Email,
        }
        template = JINJA_ENVIRONMENT.get_template('newUsers.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/newUsers',newUsers),
], debug=True)
