from google.appengine.ext import ndb

class followerfollowing(ndb.Model):
    userId = ndb.StringProperty()
    follower = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
