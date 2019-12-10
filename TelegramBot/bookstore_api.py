import requests


class endpoints:
	__home__ = "http://192.168.10.182:8000/"

	class get:
		def books(page=1):
			url = endpoints.__home__ + "api/books/?page=" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)
		
		def authors(page=1):
			url = endpoints.__home__ + "api/authors/?page=" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)

		def publishers(page=1):
			url = endpoints.__home__ + "api/publishers/?page=" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)


		def book_id(id=None):
			url = endpoints.__home__ + "api/books/" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)
		
		def author_id(id=None):
			url = endpoints.__home__ + "api/authors/" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)
			
		def publisher_id(id=None):
			url = endpoints.__home__ + "api/publishers/" + str(page)
			resp = requests.get(url=url, params="{'format':'api'}")
			return (resp)



class response_parsed:
	def __init__(self, response = None):
		self.response = response

	def page_header(func):
		def wrapper(self, *args, **kwargs):
			if (self.response):
				self.total_pages = self.response.json().get('count')
				self.next_page = self.response.json().get('next')
				self.prev_page = self.response.json().get('previous')
				self.data = self.response.json().get('results')
				func(self, *args, **kwargs)
				return(self)
		return (wrapper)

	@page_header
	def books(self):
		if (self.response and self.data):
			self.reply = self.data
		else:
			self.reply = "No books available right now"

	@page_header
	def authors(self):
		if (self.response and self.data):
			pass

	@page_header
	def publishers(self):
		if (self.response and self.data):
			pass