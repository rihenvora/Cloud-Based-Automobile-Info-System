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



class AddEV(webapp2.RequestHandler):
	#--------------------------------------------------
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		url=''
		url_string=''
		eletronicvehicle=''
		user = users.get_current_user()

		if user:
			EletronicVehicle_key = ndb.Key('EleVhe', user.user_id())
			eletronicvehicle = EletronicVehicle_key.get()
			eletronicvehicle=EleVhe(email_address=user.email())
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		template_values = {
			'url':url,
			'url_string':url_string,
			'user' : user,
            'eletronicvehicle' : eletronicvehicle
		}


		template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
		self.response.write(template.render(template_values))
	#------------------------------------------------------------------


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Add':
			user = users.get_current_user()
			if user:
				EletronicVehicle_key = ndb.Key('EleVhe', user.user_id())
				eletronicvehicle = EletronicVehicle_key.get()
				eletronicvehicle = EleVhe (
					name = self.request.get('name').strip(),
					manufacturer = self.request.get('manufacturer').strip(),
					year = int(self.request.get('year').strip()),
					btrysize = int(self.request.get('btrysize').strip()),
					wltprng = int(self.request.get('wltprng').strip()),
					power = int(self.request.get('power').strip()),
					cost = int(self.request.get('cost').strip()),
					email_address = user.email().strip()
				)
				#query = eletronicvehicle.all().filter("email_address="user.email()).filter("name=",self.request.get('name')).filter("manufacturer=",self.request.get('manufacturer')).filter("year=",self.request.get('year'))
				#query=EleVhe.query(ndb.AND(EleVhe.email_address==user.email(),EleVhe.name==eletronicvehicle.name,EleVhe.manufacturer==eletronicvehicle.manufacturer,EleVhe.year==eletronicvehicle.year))
				query=EleVhe.query(ndb.AND(EleVhe.name==eletronicvehicle.name,EleVhe.manufacturer==eletronicvehicle.manufacturer,EleVhe.year==eletronicvehicle.year))
				if query.count()==0:
					welcome="Details Entered"
					eletronicvehicle.put()
				else:
					#Code to display error box to user Using Ctypes Library Which Comes with Python Installation
					print("Details Found")
			self.redirect('/')
		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
