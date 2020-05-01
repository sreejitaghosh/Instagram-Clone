import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import MyUser
from post import post
from followerfollowing import followerfollowing

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
    )

class UserTimeline(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        All_Post_Image_URL = []
        All_Post_Caption = []
        Post_Data = None
        Displaying_Username = []
        Displaying_Caption = []
        Displaying_Image = []
        length_Of_Post = []
        max_Post = 0
        length = 0
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
            followerfollowing_data = ndb.Key('followerfollowing',user.email()).get()
            email_address = [user.email()]
            if followerfollowing_data != None:
                if followerfollowing_data.following != None:
                    i = 0
                    while i < len(followerfollowing_data.following):
                        email_address.append(followerfollowing_data.following[i])
                        i = i + 1
            i = 0
            while i < len(email_address):
                Post_Data = ndb.Key('post',email_address[i]).get()
                if Post_Data != None:
                    All_Post_Caption.append(Post_Data.caption)
                    All_Post_Image_URL.append(Post_Data.photo_url)
                else:
                    All_Post_Caption.append([])
                    All_Post_Image_URL.append([])
                length_Of_Post.append(len(All_Post_Caption[i]))
                i = i + 1
            max_Post = max(length_Of_Post)
            i = 0
            while i < max_Post:
                j = 0
                while j < len(email_address):
                    if i < len(All_Post_Caption[j]):
                        Displaying_Caption.append(All_Post_Caption[j][i])
                        Displaying_Image.append(All_Post_Image_URL[j][i])
                        Displaying_Username.append(email_address[j])
                    j = j + 1
                i = i + 1
            temp_Caption = Displaying_Caption
            Displaying_Caption = []
            temp_Image = Displaying_Image
            Displaying_Image = []
            temp_Username = Displaying_Username
            Displaying_Username = []
            i = len(temp_Caption) - 1
            while i != -1:
                Displaying_Caption.append(temp_Caption[i])
                Displaying_Image.append(temp_Image[i])
                Displaying_Username.append(temp_Username[i])
                i = i - 1
            length = len(Displaying_Image)
            if length > 50:
                length = 50
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')

        template_values = {
             'url' : url,
             'url_string' : url_string,
             'user' : user,
             'Displaying_Caption' : Displaying_Caption,
             'Displaying_Image' : Displaying_Image,
             'Displaying_Username' : Displaying_Username,
             'length' : length,
        }

        template = JINJA_ENVIRONMENT.get_template('UserTimeline.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/UserTimeline',UserTimeline),
], debug=True)
