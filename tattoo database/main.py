import webapp2

app = webapp2.WSGIApplication([
	('/', 'base_page.displayArtists'),
	('/add', 'base_page.addArtists'),
	('/edit', 'base_page.editArtists'),
], debug = True)