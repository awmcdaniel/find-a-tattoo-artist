import webapp2
import json
import api_models
from google.appengine.ext import ndb

class Artists(webapp2.RequestHandler):
	# creates a new Artist entity (see api_models)
	def post(self):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		parent_key = ndb.Key(api_models.Artist, 'artist_ancestor')
		new_artist = api_models.Artist(parent = parent_key)
		name = self.request.get('name', default_value=None)
		styles = self.request.get_all('styles', default_value=None)
		city = self.request.get('city', default_value=None)
		url = self.request.get('url', default_value=None)
		
		# name, styles, and city are required fields in the database
		if name:
			new_artist.name = name
		else:
			message = "A name is required to add an artist to the database"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return
		if styles:
			new_artist.styles = styles
		else:
			message = "At least 1 style is required to add an artist to the database"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return
		if city:
			new_artist.city = city
		else:
			message = "A city is required to add an artist to the database"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return
		if url:
			new_artist.url = url

		new_artist.put()
		output = new_artist.to_dict()
		self.response.write(json.dumps(output))
		return
	
	#returns a specific artist, or all artist entities
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		#returns a specific Artist
		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Artist, 'artist_ancestor')
			artist_query = api_models.Artist.get_by_id(int(kwargs['id']), parent_key)
			artist_by_id = [{'name' : artist_query.name, 'styles' : artist_query.styles, 'city' : artist_query.city, 'url' : artist_query.url, 'ID' : artist_query.key.id() }]
			self.response.write(json.dumps(artist_by_id))
			return
		# returns a list of all Artist entities
		else:
			query = {}
			query = [{'name' : query_element.name, 'styles' : query_element.styles, 'city' : query_element.city, 'url' : query_element.url, 'ID' : query_element.key.id() } for query_element in api_models.Artist.query(ancestor=ndb.Key(api_models.Artist, 'artist_ancestor')).fetch()]
			self.response.write(json.dumps(query))
			return
	
	#updates a specific artist
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Artist, 'artist_ancestor')
			artist_to_update = api_models.Artist.get_by_id(int(kwargs['id']), parent_key)
			# check to be sure artist was found before trying to update it
			if artist_to_update:
				name = self.request.get('name', default_value=None)
				styles = self.request.get_all('styles', default_value=None)
				city = self.request.get('city', default_value=None)
				url = self.request.get('url', default_value=None)
				
				#update artist properties if present
				if name:
					artist_to_update.name = name
				if styles:
					artist_to_update.styles = styles
				if city:
					artist_to_update.city = city
				if url:
					artist_to_update.url = url
				
				artist_to_update.put()
				self.response.write('Artist with ID: ' + kwargs['id'] + ' was successfully updated')
				return
			# if artist not found in database, return an error
			else:
				message = 'Artist with ID: ' + kwargs['id'] + ' not found'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)
				return
		else:
			message = "ID required to update artist"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

	#deletes a specific artist	
	def delete(self, **kwargs):	
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Artist, 'artist_ancestor')
			artist_to_delete = api_models.Artist.get_by_id(int(kwargs['id']), parent_key)
			# check to be sure artist was found before trying to delete it
			if artist_to_delete:
				# get studios to check for artist_to_delete
				studios_query = api_models.Studio.query().fetch()
				# update associated_artists by removing references to artist ID
				for studio in studios_query:
					if len(studio.associated_artists) > 0:
						studio.associated_artists = [artist_ID for artist_ID in studio.associated_artists if artist_ID != kwargs['id']]
					studio.put()	

				artist_to_delete.key.delete()
				self.response.write('Artist with ID: ' + kwargs['id'] + ' was successfully deleted')
				return
			# if artist not found in database, return an error
			else:
				message = 'Artist with ID: ' + kwargs['id'] + ' not found'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)
				return
		else:
			message = "ID required to delete artist"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

class Studios(webapp2.RequestHandler):
	# creates a new studio entity (see api_models)
	def post(self):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		parent_key = ndb.Key(api_models.Studio, 'studio_ancestor')
		new_studio = api_models.Studio(parent = parent_key)
		name = self.request.get('name', default_value=None)
		address = self.request.get('address', default_value=None)
		url = self.request.get('url', default_value=None)
		associated_artists = self.request.get_all('associated_artists', default_value=None)
		                                                                                                                                 
		# name is a required field in the database
		if name:
			new_studio.name = name
		else:
			message = "A name is required to add a studio to the database"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return
		if address:
			new_studio.address = address	
		if url:
			new_studio.url = url
		if associated_artists:
			new_studio.associated_artists = associated_artists

		new_studio.put()
		output = new_studio.to_dict()
		self.response.write(json.dumps(output))
		return

	#returns a specific studio, or all studio entities
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		#return a specific studio
		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Studio, 'studio_ancestor')
			studio_query = api_models.Studio.get_by_id(int(kwargs['id']), parent_key)
			studio_by_id = [{'name' : studio_query.name, 'address' : studio_query.address, 'url' : studio_query.url, 'associated_artists' : studio_query.associated_artists, 'ID' : studio_query.key.id() }]
			self.response.write(json.dumps(studio_by_id))
			return
		# returns a list of all studio entities
		else:
			query = {}
			query = [{'name' : query_element.name, 'address' : query_element.address, 'url' : query_element.url, 'associated_artists' : query_element.associated_artists, 'ID' : query_element.key.id() } for query_element in api_models.Studio.query(ancestor=ndb.Key(api_models.Studio, 'studio_ancestor')).fetch()]
			self.response.write(json.dumps(query))
			return

	#updates a specific studio
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Studio, 'studio_ancestor')
			studio_to_update = api_models.Studio.get_by_id(int(kwargs['id']), parent_key)
			# check to be sure studio was found before trying to update it
			if studio_to_update:
				name = self.request.get('name', default_value=None)
				address = self.request.get('address', default_value=None)
				url = self.request.get('url', default_value=None)
				associated_artists = self.request.get_all('associated_artists', default_value=None)
				
				#update studio properties if present
				if name:
					studio_to_update.name = name
				if address:
					studio_to_update.address = address
				if url:
					studio_to_update.url = url
				if associated_artists:
					studio_to_update.associated_artists = associated_artists
				
				studio_to_update.put()
				self.response.write('Studio with ID: ' + kwargs['id'] + ' was successfully updated')
				return
			# if studio not found in database, return an error
			else:
				message = 'Studio with ID: ' + kwargs['id'] + ' not found'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)
				return
		else:
			message = "ID required to update studio"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

	#deletes a specific studio	
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			message = "API only supports application/json MIME type"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return

		if 'id' in kwargs:
			parent_key = ndb.Key(api_models.Studio, 'studio_ancestor')
			studio_to_delete = api_models.Studio.get_by_id(int(kwargs['id']), parent_key)
			# check to be sure studio was found before trying to delete it
			if studio_to_delete:
				studio_to_delete.key.delete()
				self.response.write('Studio with ID: ' + kwargs['id'] + ' was successfully deleted')
				return
			# if studio not found in database, return an error
			else:
				message = 'Studio with ID: ' + kwargs['id'] + ' not found'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)
				return
		else:
			message = "ID required to delete studio"
			self.response.status = 400
			self.response.status_message = message
			self.response.write(message)
			return