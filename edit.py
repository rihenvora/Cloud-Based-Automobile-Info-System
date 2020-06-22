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



class EditEV(webapp2.RequestHandler):
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
		if user:
			EletronicVehicle_key = ndb.Key('EleVhe',list1 )
			EletronicVehicle_key1 = ndb.Key('EleVhe', user.user_id())
			eletronicvehicle = EletronicVehicle_key1.get()
			eletronicvehicle=EleVhe(email_address=user.email())

			url=users.create_logout_url(self.request.uri)
			url_string='logout'
			list=EleVhe.query(EleVhe.key==EletronicVehicle_key).fetch()
			#list1=eletronicvehicle
		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		template_values = {
			'url':url,
			'url_string':url_string,
			'user' : user,
			'showList':list,
			'list1':EletronicVehicle_key,
            'eletronicvehicle' : eletronicvehicle
		}


		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))
	#------------------------------------------------------------------

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Update':
			user = users.get_current_user()
			url=''
			url_string=''
			list1=''
			eletronicvehicle=''
			emial_address=''
			EletronicVehicle_key=''
			if user:
				EletronicVehicle_key = ndb.Key('EleVhe', int(self.request.get('edit_key')))
				eletronicvehicle = EletronicVehicle_key.get()
				name = self.request.get('name')
				manufacturer = self.request.get('manufacturer')
				year = int(self.request.get('year'))
				btrysize = int(self.request.get('btrysize'))
				wltprng = int(self.request.get('wltprng'))
				power = int(self.request.get('power'))
				cost = int(self.request.get('cost'))
				email_address = self.request.get('email_address')

				eletronicvehicle.name = self.request.get('name')
				eletronicvehicle.manufacturer = self.request.get('manufacturer')
				eletronicvehicle.year = int(self.request.get('year'))
				eletronicvehicle.btrysize = int(self.request.get('btrysize'))
				eletronicvehicle.wltprng = int(self.request.get('wltprng'))
				eletronicvehicle.power = int(self.request.get('power'))
				eletronicvehicle.cost = int(self.request.get('cost'))
				#eletronicvehicle.email_address = self.request.get('email_address')
				#query = eletronicvehicle.all().filter("email_address="user.email()).filter("name=",self.request.get('name')).filter("manufacturer=",self.request.get('manufacturer')).filter("year=",self.request.get('year'))
				#query=EleVhe.query(ndb.AND(EleVhe.email_address==email_address,EleVhe.name==name,EleVhe.manufacturer==manufacturer,EleVhe.year==year,EleVhe.key!=EletronicVehicle_key))
				query=EleVhe.query(ndb.AND(EleVhe.name==name,EleVhe.manufacturer==manufacturer,EleVhe.year==year,EleVhe.key!=EletronicVehicle_key))
				if query.count()>=1:
					welcome="Details Already Entered"
					#eletronicvehicle.put()
				else:
					#Code to display error box to user Using Ctypes Library Which Comes with Python Installation
					#print("Details Found")
					eletronicvehicle.put()
			self.redirect('/')
		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
