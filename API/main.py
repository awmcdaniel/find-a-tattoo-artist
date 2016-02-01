import webapp2

app = webapp2.WSGIApplication([
	('/artists', 'api.Artists'),
	('/studios', 'api.Studios'),
], debug = True)

app.router.add(webapp2.Route(r'/artists/<id:[0-9]+><:/?>', 'api.Artists'))
app.router.add(webapp2.Route(r'/studios/<id:[0-9]+><:/?>', 'api.Studios'))