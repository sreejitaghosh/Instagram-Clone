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
        length = 0
        userfollower = 0
        userfollowing = 0
        userfollower1 = 0
        userfollowing1 = 0
        newEmail = self.request.get('email_address')
        newUsers = ndb.Key('MyUser',newEmail).get()
        user = users.get_current_user()
        followDecission = "False"
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

            collection_key = ndb.Key('post',newUsers.userId)
            collection_key = collection_key.get()
            if collection_key != None:
                i = len(collection_key.photo_url) - 1
                while i > -1:
                    collection.append(collection_key.photo_url[i])
                    Caption.append(collection_key.caption[i])
                    i = i - 1
                length = len(collection)
            newUserFFList = ndb.Key('followerfollowing',newEmail).get()
            if newUserFFList != None:
                userfollower = len(newUserFFList.follower)
                userfollowing = len(newUserFFList.following)
            oldUsersEmail =  myuser.email_address
            collect = ndb.Key('followerfollowing',oldUsersEmail).get()
            if collect != None:
                for i in collect.following:
                    if i == newEmail:
                        followDecission = 'True'
                        break
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'collection' : collection,
             'Caption' : Caption,
             'length' : length,
             'newUsers' : newUsers,
             'newEmail' : newEmail,
             'userfollower': userfollower,
             'userfollowing': userfollowing,
             'userfollower1': userfollower1,
             'userfollowing1': userfollowing1,
             'followDecission' : followDecission,
        }
        template = JINJA_ENVIRONMENT.get_template('newUsers.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        new_Email = self.request.get('email_address')
        new_Users = ndb.Key('MyUser',new_Email).get()
        collect_ff_new = ndb.Key('followerfollowing',new_Users.email_address).get()

        old_Email = user.email()
        old_Users = ndb.Key('MyUser',old_Email).get()
        collect_ff_old = ndb.Key('followerfollowing',old_Users.email_address).get()

        button = self.request.get('submit')

        if button == 'Follow':
            if new_Email != old_Email:
                if collect_ff_old != None:
                    collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()
                else:
                    collect_ff_old = followerfollowing(id=old_Email)
                    collect_ff_old.following.append(new_Email)
                    collect_ff_old.put()

                if collect_ff_new != None:
                    collect_ff_new.follower.append(user.email())
                    collect_ff_new.put()
                else:
                    collect_ff_new = followerfollowing(id=new_Email)
                    collect_ff_new.follower.append(user.email())
                    collect_ff_new.put()
            self.redirect('/newUsers?email_address='+new_Email)

        elif button == 'Unfollow':
            if len(collect_ff_old.following) == 1:
                ndb.Key('followerfollowing',old_Email).delete()
            else:
                for i in range(0,len(collect_ff_old.following)):
                    if collect_ff_old.following[i] == new_Email:
                        del collect_ff_old.following[i]
                        collect_ff_old.put()
                        break
            if len(collect_ff_new.follower) == 1:
                ndb.Key('followerfollowing',new_Email).delete()
            else:
                for l in range(0,len(collect_ff_new.follower)):
                    if collect_ff_new.follower[l] == old_Email:
                        del collect_ff_new.follower[l]
                        collect_ff_new.put()
                        break
            self.redirect('/newUsers?email_address='+new_Email)

app = webapp2.WSGIApplication([
('/newUsers',newUsers),
], debug=True)
