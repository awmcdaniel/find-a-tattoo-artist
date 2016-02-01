from google.appengine.ext import ndb

class Artist(ndb.Model):
	name = ndb.StringProperty(required=True)
	styles = ndb.StringProperty(repeated=True)
	city = ndb.StringProperty(required=True)
	url = ndb.StringProperty()
	email = ndb.StringProperty()
	rating = ndb.IntegerProperty()
	comment = ndb.TextProperty()