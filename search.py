import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from eletronicvehicle import EleVhe


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)



class Search(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		# URL that will contain a login or logout link
		# and also a string to represent this
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		eletronicvehicle = ''
		template_values = ''
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
		template = JINJA_ENVIRONMENT.get_template('search.html')
		#template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = "text/html"


		if self.request.get('button') =="Search":
			url = ''
			url_string = ''
			welcome = 'Welcome back'
			eletronicvehicle = ''
			list = ''
			list1=''
			name=''
			email_address=''
			manufacturer=''
			year=0 #min value of year
			year1=0 #max value of year
			btrysize=0 #min value of betery size
			btrysize1=0 #max value of betery size
			wltprng=0 #min value of WLTP range
			wltprng1=0 #max value of WLTP range
			cost=0 #min value of cost
			cost1=0 #max value of cost1
			power=0 #min value of Power
			power1=0 #max value of Power

			template_values=''

			user = users.get_current_user()

			if user:
				url = users.create_logout_url(self.request.uri)
				url_string = 'logout'
				EletronicVehicle_key = ndb.Key('EleVhe', user.user_id())
				eletronicvehicle = EletronicVehicle_key.get()
				query = EleVhe.query(EleVhe.email_address == user.email()).get()

				if eletronicvehicle == '' and query== None:
					welcome = 'Welcome to  the Application'
					eletronicvehicle = EleVhe(id=user.user_id())
					eletronicvehicle = EleVhe(email_address=user.email())
				else:
					welcome = 'Welcome Back'
					eletronicvehicle = EleVhe(email_address=user.email())
			else:
				url = users.create_login_url(self.request.uri)
				url_string = 'login'

			#print("--------"+self.request.get('name'))
			list = EleVhe.query()

			if(self.request.get('name').strip() != '' and self.request.get('name').strip() != None):
				name = self.request.get('name').strip()
			if(self.request.get('manufacturer').strip() !='' and self.request.get('manufacturer').strip() != None ):
				manufacturer = self.request.get('manufacturer').strip()
			if(self.request.get('year').strip() !='' and self.request.get('year').strip() != None ):
				year = int(self.request.get('year'))
			if(self.request.get('year1').strip() !='' and self.request.get('year1').strip() != None ):
				year1 = int(self.request.get('year1'))
			if(self.request.get('btrysize').strip() != '' and self.request.get('btrysize').strip() != None):
				btrysize = int(self.request.get('btrysize'))
			if(self.request.get('btrysize1').strip() != '' and self.request.get('btrysize1').strip() != None):
				btrysize1 = int(self.request.get('btrysize1'))
			if(self.request.get('wltprng').strip() != '' and self.request.get('wltprng').strip() != None):
				wltprng = int(self.request.get('wltprng'))
			if(self.request.get('wltprng1').strip() != '' and self.request.get('wltprng1').strip() != None):
				wltprng1 = int(self.request.get('wltprng1'))
			if(self.request.get('power').strip() != '' and self.request.get('power').strip() != None):
				power = int(self.request.get('power'))
			if(self.request.get('power1').strip() != '' and self.request.get('power1').strip() != None):
				power1 = int(self.request.get('power1'))
			if(self.request.get('cost').strip() != '' and self.request.get('cost').strip() != None):
				cost = int(self.request.get('cost'))
			if(self.request.get('cost1').strip() != '' and self.request.get('cost1').strip() != None):
				cost1 = int(self.request.get('cost1'))
			if(self.request.get('email_address').strip() != '' and self.request.get('email_address').strip() != None):
				email_address = self.request.get('email_address').strip()


			if( name=='' and manufacturer == '' and email_address =='' and year == 0 and year1 == 0 and btrysize == 0 and btrysize1 == 0 and wltprng == 0 and wltprng1 == 0 and power == 0 and power1 == 0 and cost == 0 and cost1 == 0 ):
				#list1 = type(cost)
				list = list.filter()
			else:
				#list1= cost
				list = list.filter(ndb.OR(EleVhe.name == name,EleVhe.manufacturer == manufacturer,ndb.AND(EleVhe.year >= year,EleVhe.year <= year1),ndb.AND(EleVhe.btrysize >= btrysize,EleVhe.btrysize <= btrysize1),ndb.AND(EleVhe.wltprng >= wltprng,EleVhe.wltprng <= wltprng1),ndb.AND(EleVhe.power >= power,EleVhe.power <= power1),ndb.AND(EleVhe.cost >= cost,EleVhe.cost <= cost1),EleVhe.email_address == email_address))

			#list1 = list
			list = list.fetch()

			#list1 = list

			template_values={
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'eletronicvehicle' : eletronicvehicle,
			'showList' : list,
			'list1' : list1
			}

			template = JINJA_ENVIRONMENT.get_template('search.html')
			self.response.write(template.render(template_values))
