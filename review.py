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


class Review(webapp2.RequestHandler):
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
        if(self.request.get('message') != ''):
            message=self.request.get('message')
        else:
            message=''
        list=''
        listr=''
        avgl=[]
        avg=0.0
        EletronicVehicle_key = ndb.Key('EleVhe',list1)
        list=EleVhe.query(EleVhe.key==EletronicVehicle_key).fetch()
        listr=Reviews.query(Reviews.vehicle_id==list1).order(-Reviews.sequence).fetch()
        for i in listr:
            avgl.append(i.rating)
            avg+=int(i.rating)
        if len(avgl)>0:
            avg=avg/len(avgl)
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
        'Review':listr,
        'Avg':avg,
        'message':message,
        'list1':list1,
        'eletronicvehicle' : eletronicvehicle
        }

        template = JINJA_ENVIRONMENT.get_template('Review.html')
        self.response.write(template.render(template_values))
            #------------------------------------------------------------------
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Save':
            url=''
            url_string=''
            list1=''
            eletronicvehicle=''
            EletronicVehicle_key=''
            message=''
            review=''
            user = users.get_current_user()
            #list1=self.request.get('key').strip("Key()").split(",")
            list1=int(self.request.get('hiddenid').strip())
            message=self.request.get('message')
            message=''
            list=''
            listr=''
            avgl=[]
            avg=0
            rcnt=''
            EletronicVehicle_key = ndb.Key('EleVhe',list1)
            list=EleVhe.query(EleVhe.key==EletronicVehicle_key).fetch()
            user = users.get_current_user()
            if user:
                EletronicVehicle_key = ndb.Key('EleVhe', user.user_id())
                eletronicvehicle = EletronicVehicle_key.get()
                eletronicvehicle=EleVhe(email_address=user.email())
                listr=Reviews.query(Reviews.vehicle_id==list1)
                rcnt=listr.count()
                review = Reviews (
                review = self.request.get('review').strip(),
                rating = int(self.request.get('rating').strip()),
                vehicle_id = int(self.request.get('hiddenid').strip()),
                email_address = user.email().strip(),
                sequence = rcnt
                )
                if len(self.request.get('review').strip())<=1000:
                    review.put()
                else:
                    self.redirect('/?message=Review Length Exceeds')
            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'
            self.redirect('/')
        elif self.request.get('button') == 'Cancel':
			self.redirect('/')
