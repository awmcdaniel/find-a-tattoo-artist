import webapp2
import os
import jinja2
from google.appengine.ext import ndb

# set up Artist class for database
class Artist(ndb.Model):
	name = ndb.StringProperty(required=True)
	styles = ndb.StringProperty(repeated=True)
	city = ndb.StringProperty(required=True)
	url = ndb.StringProperty()
	email = ndb.StringProperty()
	tattoo_bool = ndb.StringProperty()
	rating = ndb.IntegerProperty()
	comment = ndb.TextProperty()

# set up jinja2 environment, point it to our templates
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
	)

# queries the database and displays all artists
class displayArtists(webapp2.RequestHandler):
	def get(self):
		template_variables = {}
		template = JINJA_ENVIRONMENT.get_template('display_all.html')
		template_variables['artists'] = [{'artist_name' : query_element.name, 'artist_style' : query_element.styles, 'artist_city' : query_element.city, 'artist_url' : query_element.url, 'artist_email' : query_element.email, 'tattoo_bool' : query_element.tattoo_bool, 'artist_rating' : query_element.rating, 'artist_comments' : query_element.comment, 'key': query_element.key.urlsafe() } for query_element in Artist.query(ancestor=ndb.Key(Artist, 'default')).fetch()]
		self.response.write(template.render(template_variables)) 

	#could expand with a post definition that allows queries by parameters
	#def post(self):

# allows user to add an artist to the database
class addArtists(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add_artist.html')
		self.response.write(template.render())

	def post(self):
		parent_key = ndb.Key(Artist, 'default')
		artist = Artist(parent = parent_key)
		artist.name = self.request.get('artist_name')
		artist.styles = self.request.get_all('artist_style[]')
		# artist.styles = [element for element in self.request.get_all('artist_style[]')]
		artist.city = self.request.get('artist_city')
		artist.url = self.request.get('artist_url')
		artist.email = self.request.get('artist_email')
		artist.tattoo_bool = self.request.get('tattoo_bool')
		# convert artist rating from string to int
		artist.rating = int(self.request.get('artist_rating'))
		artist.comment = self.request.get('artist_comments')
		# write to datastore
		artist.put()
		# redirect user to display all artists
		self.redirect('/')

# allows user to edit an artist in the database
class editArtists(webapp2.RequestHandler):
	def get(self):
		template_variables = {}
		template = JINJA_ENVIRONMENT.get_template('edit_artist.html')
		artist_key = ndb.Key(urlsafe=self.request.get('key'))
		artist = artist_key.get()
		template_variables['artist'] = [{'artist_name' : artist.name, 'artist_style' : artist.styles, 'artist_city' : artist.city, 'artist_url' : artist.url, 'artist_email' : artist.email, 'tattoo_bool' : artist.tattoo_bool, 'artist_rating' : artist.rating, 'artist_comments' : artist.comment}]
		self.response.write(template.render(template_variables))

	def post(self):
		artist_key = ndb.Key(urlsafe=self.request.get('key'))
		artist = artist_key.get()
		artist.name = self.request.get('artist_name')
		artist.styles = self.request.get_all('artist_style[]')
		artist.city = self.request.get('artist_city')
		artist.url = self.request.get('artist_url')
		artist.email = self.request.get('artist_email')
		artist.rating = int(self.request.get('artist_rating'))
		artist.comment = self.request.get('artist_comments')
		artist.put()
		self.redirect('/edit?key=' + artist_key.urlsafe())