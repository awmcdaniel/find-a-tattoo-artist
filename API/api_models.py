from google.appengine.ext import ndb

# set up Artist class for database
class Artist(ndb.Model):
	name = ndb.StringProperty(required=True)
	styles = ndb.StringProperty(repeated=True)
	city = ndb.StringProperty(required=True)
	url = ndb.StringProperty()

# set up Studio class for database
class Studio(ndb.Model):
	name = ndb.StringProperty(required=True)
	address = ndb.StringProperty()
	url = ndb.StringProperty()
	associated_artists = ndb.StringProperty(repeated=True)