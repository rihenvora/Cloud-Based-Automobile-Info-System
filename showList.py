from google.appengine.ext import ndb

class showList(ndb.Model):
    Name = ndb.StringProperty(repeated=True)
