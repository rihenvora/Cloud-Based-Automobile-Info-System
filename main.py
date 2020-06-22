import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import urlparse

from eletronicvehicle import EleVhe,Reviews
from add import AddEV
from search import Search
from edit import EditEV
from delete import DeleteEV
from Details import Details
from review import Review

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        eletronicvehicle = ''
        list = ''
        # pull the current user from the request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            EletronicVehicle_key = ndb.Key('EleVhe', user.user_id())
            eletronicvehicle = EletronicVehicle_key.get()
            query = EleVhe.query(EleVhe.email_address == user.email()).get() #Query To GetUser Email Address

            if eletronicvehicle == '' and query== None:
                welcome = 'Welcome to  the Application'
                eletronicvehicle = EleVhe(id=user.user_id())
                eletronicvehicle = EleVhe(email_address=user.email())
                #eletronicvehicle.put()
            else:
                welcome = 'Welcome Back'
                eletronicvehicle = EleVhe(email_address=user.email())

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        list = EleVhe.query().fetch()
        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'eletronicvehicle' : eletronicvehicle,
            'showList' : list
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type']='text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'
        eletronicvehicle = ''
        list = ''

        action = self.request.get('button')
        if action == 'Delete':
            index= self.request.get(key_id)

            list= index

        template_values={
            'list':list
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))

class Compare(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        ids=''
        list1=''
        listr=''
        l1=[]
        l2=[]
        cost=[]
        maxcost=0
        wltp=[]
        maxwltp=0
        power=[]
        maxpower=0
        btrysize=[]
        avgrating=[]
        maxavg=0
        maxbtry=0
        list2=''
        list = EleVhe.query()
        if self.request.get('button') == 'Compare':
            for i in range(list.count()):
                if(self.request.get("check_"+str(i))):
                    #l1.append(ndb.Key('EleVhe', self.request.get("check_"+str(i)).strip()))
                    l1.append(int(self.request.get("check_"+str(i)).strip()))

            if len(l1)<2:
                self.redirect('/')
            else:
                for j in range(len(l1)):
                    list1=EleVhe.query(EleVhe.key==ndb.Key('EleVhe',l1[j]))
                    c=0
                    avg=0.0
                    listr=Reviews.query(Reviews.vehicle_id==l1[j]).fetch()
                    for m in listr:
                        c+=1
                        avg+=int(m.rating)
                    if c>0:
                        avg=avg/c
                    else:
                        avg=0
                    avgrating.append(avg)
                    l2.append(list1.fetch())
                    #l2.append(avg)
                for k in l2:
                    for l in k:
                        cost.append(l.cost)
                        wltp.append(l.wltprng)
                        power.append(l.power)
                        btrysize.append(l.btrysize)
                maxcost=max(cost)
                maxwltp=max(wltp)
                maxpower=max(power)
                maxbtry=max(btrysize)
                maxavg=max(avgrating)
        template_values={
            'showList':l2,
            'cost':maxcost,
            'list1':list2,
            'wltp': maxwltp,
            'power':maxpower,
            'btrysize':maxbtry,
            'avgrat':maxavg,
            'avgratl':avgrating
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', AddEV),
    ('/search', Search),
    ('/edit', EditEV),
    ('/delete', DeleteEV),
    ('/Compare', Compare),
    ('/Details', Details),
    ('/review', Review),
], debug=True)
