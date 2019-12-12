import requests
import re


class endpoints:
	__home__ = "http://192.168.10.182:8000/"
	books_page = __home__ + "api/books/?page="
	authors_page = __home__ + "api/authors/?page="
	publishers_page = __home__ + "api/publishers/?page="

	class get:
		def books(page=1):
			url = endpoints.books_page + str(page)
			resp = requests.get(url=url)
			return (resp)
		
		def authors(page=1):
			url = endpoints.authors_page + str(page)
			resp = requests.get(url=url)
			return (resp)

		def publishers(page=1):
			url = endpoints.publishers_page + str(page)
			resp = requests.get(url=url)
			return (resp)


		def book_id(id=None):
			url = endpoints.__home__ + "api/books/" + str(page)
			resp = requests.get(url=url)
			return (resp)
		
		def author_id(id=None):
			url = endpoints.__home__ + "api/authors/" + str(page)
			resp = requests.get(url=url)
			return (resp)
			
		def publisher_id(id=None):
			url = endpoints.__home__ + "api/publishers/" + str(page)
			resp = requests.get(url=url)
			return (resp)



class callback_handle:
	def query(call):
		message = call.message.text
		if (re.search(r'Books on page \d+', message)):
			page = re.search(r'Books on page \d+', message).group().split(' ')[-1]
			resp = endpoints.get.books(page=page)
			resp_parsed = response_parsed(response=resp).books()
			return (resp_parsed)

		elif (re.search(r'Authors on page \d+', message)):
			page = re.search(r'Authors on page \d+', message).group().split(' ')[-1]
			resp = endpoints.get.authors(page=page)
			resp_parsed = response_parsed(response=resp).authors()
			return (resp_parsed)

		elif (re.search(r'Publishers on page \d+', message)):
			page = re.search(r'Publishers on page \d+', message).group().split(' ')[-1]
			resp = endpoints.get.publishers(page=page)
			resp_parsed = response_parsed(response=resp).publishers()
			return (resp_parsed)



class response_parsed:
	def __init__(self, response = None):
		self.response = response if response else None
		self.reply = "No items right now"
		self.ok = True if self.response else False
		self.query_type = None

	def page_header(func):
		def wrapper(self, *args, **kwargs):
			if (self.ok):
				self.total = self.response.json().get('count')
				self.next_page = int(re.search(r'=\d+', self.response.json().get('next')).group()[1:]) if self.response.json().get('next') else None
				self.prev_page = None
				if (self.response.json().get('previous')):
					if (re.search(r'=\d+', self.response.json().get('previous'))):
						self.prev_page = int(re.search(r'=\d+', self.response.json().get('previous')).group()[1:])
					else:
						self.prev_page = 1
				self.current_page = self.prev_page + 1 if self.prev_page else 1
				self.data = self.response.json().get('results')
				func(self, *args, **kwargs)
				return(self)
			return(self)
		return (wrapper)



	@page_header
	def books(self):
		if (self.ok and self.data):
			self.query_type = "Books"
			self.on_page = len(self.data)
			self.reply = self.query_type + " on page %s:\n\n" % str(self.current_page)
			for index, book in enumerate(self.data):
				self.reply = self.reply + str(index + 1) + ". " + book.get("name") + " (" \
					+ "published in " + str(book.get("year")) + ")\n"

	@page_header
	def authors(self):
		if (self.ok and self.data):
			self.query_type = "Authors"
			self.on_page = len(self.data)
			self.reply = self.query_type + " on page %s:\n\n" % str(self.current_page)
			for index, author in enumerate(self.data):
				self.reply = self.reply + str(index + 1) + ". " + author.get("name") +"\n"

	@page_header
	def publishers(self):
		if (self.ok and self.data):
			self.query_type = "Publishers"
			self.on_page = len(self.data)
			self.reply = self.query_type + " on page %s:\n\n" % str(self.current_page)
			for index, publisher in enumerate(self.data):
				self.reply = self.reply + str(index + 1) + ". " + publisher.get("name") + (" (" \
					+ str(publisher.get("notes")[:50]) + "...)\n") if publisher.get("notes") else "\n"


