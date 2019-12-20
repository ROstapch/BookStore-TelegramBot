import requests
import re
import os
from settings import MEDIA_ROOT



class Endpoints:

	__home__ = "http://192.168.10.182:8000/"
	books = __home__ + "api/books/"
	books_page = __home__ + "api/books/?page="
	authors = __home__ + "api/authors/"
	authors_page = __home__ + "api/authors/?page="
	publishers = __home__ + "api/publishers/"
	publishers_page = __home__ + "api/publishers/?page="

	class get:

		def books(page=1):
			url = Endpoints.books_page + str(page)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None
		
		def authors(page=1):
			url = Endpoints.authors_page + str(page)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None

		def publishers(page=1):
			url = Endpoints.publishers_page + str(page)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None


		def book_id(item_id=None):
			url = Endpoints.__home__ + "api/books/" + str(item_id)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None
		
		def author_id(id=None):
			url = Endpoints.__home__ + "api/authors/" + str(item_id)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None
			
		def publisher_id(id=None):
			url = Endpoints.__home__ + "api/publishers/" + str(item_id)
			try:
				resp = requests.get(url=url)
				return (resp)
			except Exception:
				return None

	class post:

		def book(book):
			url = Endpoints.books
			try:
				resp = None
				if (book.cover):
					resp = requests.post(url = url, params={"type":"multipart/form-data"},\
						data = book.to_dic(), files={"photo": open(book.cover, 'rb')})
					if (resp):
						os.remove(book.cover)
				else:
					resp = requests.post(url = url, data = book.to_dic(), params={"type":"application/json"})
				return (resp)
			except Exception:
				return None
		
		def author(author):
			url = Endpoints.authors
			try:
				resp = None
				if (author.photo):
					resp = requests.post(url = url, params={"type":"multipart/form-data"},\
						data = author.to_dic(), files={"photo": open(author.photo, 'rb')})
					if (resp):
						os.remove(author.photo)
				else:
					resp = requests.post(url = url, data = author.to_dic(), params={"type":"application/json"})
				return (resp)
			except Exception:
				return None

		def publisher(publisher):
			url = Endpoints.publishers
			try:
				resp = requests.post(url = url, data = publisher.to_dic(), params={"type":"application/json"})
				return (resp)
			except Exception:
				return None

	class delete:

		def item_by_url(url):
			try:
				resp = requests.delete(url=url)
				return (resp)
			except Exception:
				return None

		def book_id(item_id=None):
			url = Endpoints.__home__ + "api/books/" + str(item_id)
			try:
				resp = requests.delete(url=url)
				return (resp)
			except Exception:
				return None
		
		def author_id(id=None):
			url = Endpoints.__home__ + "api/authors/" + str(item_id)
			try:
				resp = requests.delete(url=url)
				return (resp)
			except Exception:
				return None
			
		def publisher_id(id=None):
			url = Endpoints.__home__ + "api/publishers/" + str(item_id)
			try:
				resp = requests.delete(url=url)
				return (resp)
			except Exception:
				return None

	class patch:

		def patch_name(url, name):
			try:
				resp = requests.patch(url=url, params={"type":"application/json"}, data={"name":name})
				return (resp)
			except Exception:
				return None



class CallbackHandle:

	def query(call):
		message = call.message.text
		if (re.search(r'Books on page \d+', message)):
			page = re.search(r'Books on page \d+', message).group().split(' ')[-1]
			resp = Endpoints.get.books(page=page)
			resp_parsed = ResponseParsed(response=resp).books()
			return (resp_parsed)

		elif (re.search(r'Authors on page \d+', message)):
			page = re.search(r'Authors on page \d+', message).group().split(' ')[-1]
			resp = Endpoints.get.authors(page=page)
			resp_parsed = ResponseParsed(response=resp).authors()
			return (resp_parsed)

		elif (re.search(r'Publishers on page \d+', message)):
			page = re.search(r'Publishers on page \d+', message).group().split(' ')[-1]
			resp = Endpoints.get.publishers(page=page)
			resp_parsed = ResponseParsed(response=resp).publishers()
			return (resp_parsed)

	def item_url(call):
		message = call.message.text
		if (re.search(r'Book\(id_\d+\)', message)):
			item_id = re.search(r'Book\(id_\d+\)', message).group()[8:-1]
			return (Endpoints.books + item_id + '/')

		elif (re.search(r'Author\(id_\d+\)', message)):
			item_id = re.search(r'Author\(id_\d+\)', message).group()[10:-1]
			return (Endpoints.authors + item_id + '/')

		elif (re.search(r'Publisher\(id_\d+\)', message)):
			item_id = re.search(r'Publisher\(id_\d+\)', message).group()[13:-1]
			return (Endpoints.publishers + item_id + '/')



class ResponseParsed:

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
				return (self)
			return (self)
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
					+ str(publisher.get("notes")[:20]) + "...)\n") if publisher.get("notes") else "\n"


	def item_on_page(self, id_on_page):
		reply = "Couldn't find requested item"
		if (self.ok and self.data and self.query_type == "Books"):
			book = self.data[id_on_page]
			book_id = book.get('id')
			book_name = book.get('name')
			book_cover = book.get('cover') if book.get('cover') else 'No cover image available'
			book_pages = str(book.get('pages')) if book.get('pages') else 'no info'
			book_year = str(book.get('year')) if book.get('year') else 'no info'

			book_authors = ''
			authors = book.get('author')
			for index, author in enumerate(authors):
				temp_response = requests.get(url=author)
				if (temp_response):
					author_name = temp_response.json().get('name')
					book_authors = book_authors + "%d. %s\n" % (index + 1, author_name)

			book_publishers = ''
			publishers = book.get('publisher')
			for index, publisher in enumerate(publishers):
				temp_response = requests.get(url=publisher)
				if (temp_response):
					publisher_name = temp_response.json().get('name')
					book_publishers = book_publishers + "%d. %s\n" % (index + 1, publisher_name)

			reply = "Book(id_%d):\n\nName: %s\n\nAuthor(s):\n%s\nPublisher(s):\n%s" % (book_id, book_name, book_authors, book_publishers) + \
			 "\nPublished in %s year\n%s pages\n\nBook cover:\n%s" % (book_year, book_pages, book_cover)

		elif (self.ok and self.data and self.query_type == "Authors"):
			author = self.data[id_on_page]
			author_id = author.get('id')
			author_name = author.get('name')
			author_photo = author.get('photo') if author.get('photo') else 'No photo available'
			author_birth = str(author.get('date_of_birth')) if author.get('date_of_birth') else 'no info'

			reply = "Author(id_%d):\n\nName: %s\nDate of birth: %s\n\n%s" % (author_id, author_name, author_birth, author_photo)

		elif (self.ok and self.data and self.query_type == "Publishers"):
			publisher = self.data[id_on_page]
			publisher_id = publisher.get('id')
			publisher_name = publisher.get('name')
			publisher_notes = publisher.get('notes') if publisher.get('notes') else 'No notes'

			reply = "Publisher(id_%d):\n\nName: %s\nNotes: %s" % (publisher_id, publisher_name, publisher_notes)
		return (reply)



def get_page(page=1, query_type=None):
	resp_parsed = None
	if (query_type == "Books"):
		resp = Endpoints.get.books(page=page)
		resp_parsed = ResponseParsed(response=resp).books()
	elif (query_type == "Authors"):
		resp = Endpoints.get.authors(page=page)
		resp_parsed = ResponseParsed(response=resp).authors()
	elif (query_type == "Publishers"):
		resp = Endpoints.get.publishers(page=page)
		resp_parsed = ResponseParsed(response=resp).publishers()
	return (resp_parsed)



class Models:

	class Publisher:

		def __init__(self, name):
			self.name = name
			self.notes = None

		def to_dic(self):
			publisher = {"name":self.name, "notes":self.notes}
			return (publisher)


	class Author:

		def __init__(self, name):
			self.name = name
			self.birth = None
			self.photo = None

		def to_dic(self):
			if (self.photo):
				author = {"name":self.name, "date_of_birth":self.birth.strftime("%Y-%m-%d")}
			else:
				author = {"name":self.name, "photo":self.photo, "date_of_birth":self.birth.strftime("%Y-%m-%d")}
			return (author)


	class Book:

		def __init__(self, name):
			self.name = name
			self.cover = None
			self.pages = None
			self.year = None
			self.author = None
			self.publisher = None

		def to_dic(self):
			if (self.cover):
				book = {"name":self.name, "pages":self.pages, "year":self.year,\
				"author": [Endpoints.authors + str(self.author) + '/',], \
				"publisher": [Endpoints.publishers + str(self.publisher) + '/',]}
			else:
				book = {"name":self.name, "cover":self.cover, "pages":self.pages, "year":self.year,\
				"author": [Endpoints.authors + str(self.author) + '/',], \
				"publisher": [Endpoints.publishers + str(self.publisher) + '/',]}
			return (book)

