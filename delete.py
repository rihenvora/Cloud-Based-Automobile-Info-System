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



class DeleteEV(webapp2.RequestHandler):
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


		template = JINJA_ENVIRONMENT.get_template('delete.html')
		self.response.write(template.render(template_values))
	#------------------------------------------------------------------

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Delete':
			user = users.get_current_user()
			url=''
			url_string=''
			EletronicVehicle_key=''
			if user:
				EletronicVehicle_key = ndb.Key('EleVhe', int(self.request.get('delete_key')))
				eletronicvehicle = EletronicVehicle_key.get()
				EletronicVehicle_key.delete()
			else:
				url = users.create_login_url(self.request.uri)
				url_string = 'login'
			self.redirect('/')
		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
