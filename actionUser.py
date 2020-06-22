import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os
import urlparse
from google.appengine.api import images

from instagramdb import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class actionUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        follower=self.request.get("key1") #sarched user
        action=self.request.get("key2") #action
        following=self.request.get("key3") # main user
        flow_users= [] #list of users follows for main user
        flwing_user = [] #list of users following for follower
        follower_user = ndb.Key('User',int(self.request.get("key1"))).get()
        following_user = ndb.Key('User',int(self.request.get("key3"))).get()
        if action == 0:
            follower_user.fllower.append(self.request.get("key3"))
            following_user.folows.append(self.request.get("key1"))
            follower_user.put()
            following_user.put()
        elif action == 1:
            for user in following_user.folows:
                if self.request.get("key1") != user:
                    flow_users.append(user)

            for user in follower_user.fllower:
                if self.request.get("key3") != user:
                    flwing_user.append(user)

            following_user.folows = flow_users
            following_user.put()
            follower_user.fllower = flwing_user
            follower_user.put()
        self.redirect('/details?key=',follower)
