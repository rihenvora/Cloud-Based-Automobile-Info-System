import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from eletronicvehicle import EleVhe,Reviews


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)


class Details(webapp2.RequestHandler):
    #--------------------------------------------------
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url=''
        url_string=''
        list1=''
        eletronicvehicle=''
        EletronicVehicle_key=''
        user = users.get_current_user()
        #list1=self.request.get('key').strip("Key()").split(",")
        list1=int(self.request.get('key'))
        list=''
        listr=''
        c=0
        avg=0.0
        maxavg=0.0
        EletronicVehicle_key = ndb.Key('EleVhe',list1)
        list=EleVhe.query(EleVhe.key==EletronicVehicle_key).fetch()
        listr=Reviews.query(Reviews.vehicle_id==list1).order(-Reviews.sequence).fetch()
        for m in listr:
            c+=1
            avg+=int(m.rating)
        if c>0:
            avg=avg/c
        else:
            avg=0
        if user:
            EletronicVehicle_key1 = ndb.Key('EleVhe', user.user_id())
            eletronicvehicle = EletronicVehicle_key1.get()
            eletronicvehicle=EleVhe(email_address=user.email())

            url=users.create_logout_url(self.request.uri)
            url_string='logout'
            #list1=eletronicvehicle
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
        'url':url,
        'url_string':url_string,
        'user' : user,
        'showList':list,
        'review':listr,
        'avgrat':avg,
        'list1':EletronicVehicle_key,
        'eletronicvehicle' : eletronicvehicle
        }

        template = JINJA_ENVIRONMENT.get_template('Details.html')
        self.response.write(template.render(template_values))
    #------------------------------------------------------------------
