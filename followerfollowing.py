from google.appengine.ext import ndb

class followerfollowing(ndb.Model):
    follower = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
