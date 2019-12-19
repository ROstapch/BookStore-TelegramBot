import telebot
from telebot import types
#from aiohttp import web
#import ssl
from datetime import datetime

from bot_config import *
from bookstore_api import *
from markup import *
from settings import MEDIA_ROOT


bot = telebot.TeleBot(TOKEN)



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	if call.data == "close":
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

	elif call.data in ["1" , "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
		reply_call = CallbackHandle.query(call)
		resp_parsed = get_page(reply_call.current_page, reply_call.query_type)
		reply = resp_parsed.item(int(call.data) - 1)
		bot.send_message(call.message.chat.id, text=reply, reply_markup=item_markup())

	elif call.data == "prev_page":
		reply_call = CallbackHandle.query(call)
		if(reply_call.prev_page):
			resp_parsed = get_page(reply_call.prev_page, reply_call.query_type)
			bot.edit_message_text(text=resp_parsed.reply, chat_id=call.message.chat.id,
				message_id=call.message.message_id, inline_message_id=call.inline_message_id,
				reply_markup=query_markup(resp_parsed))

	elif call.data == "next_page":
		reply_call = CallbackHandle.query(call)
		if(reply_call.next_page):
			resp_parsed = get_page(reply_call.next_page, reply_call.query_type)
			bot.edit_message_text(text=resp_parsed.reply, chat_id=call.message.chat.id,
				message_id=call.message.message_id, inline_message_id=call.inline_message_id,
				reply_markup=query_markup(resp_parsed))

	elif call.data == "update_item":
		pass

	elif call.data == "delete_item":
		pass



@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"This message will help you get along with current bot\nList of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint\n" +
		"/books - get list of all books\n" + 
		"/authors - get list of all authors\n" +
		"/publishers - get list of all publishers\n" +
		"/add_author - add new author\n" +
		"/add_publisher - add new publisher"\
		, reply_markup=markup)
	

@bot.message_handler(commands=['help'])
def send_help(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"List of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint\n" +
		"/books - get list of all books\n" + 
		"/authors - get list of all authors\n" +
		"/publishers - get list of all publishers\n" +
		"/add_author - add new author\n" +
		"/add_publisher - add new publisher"\
		, reply_markup=markup)


@bot.message_handler(commands=['books'])
def list_books(message):
	resp_parsed = get_page(1, "Books")
	bot.send_message(message.chat.id, resp_parsed.reply, reply_markup=query_markup(resp_parsed))


@bot.message_handler(commands=['authors'])
def list_books(message):
	resp_parsed = get_page(1, "Authors")
	bot.send_message(message.chat.id, resp_parsed.reply, reply_markup=query_markup(resp_parsed))


@bot.message_handler(commands=['publishers'])
def list_books(message):
	resp_parsed = get_page(1, "Publishers")
	bot.send_message(message.chat.id, resp_parsed.reply, reply_markup=query_markup(resp_parsed))


@bot.message_handler(commands=['add_book'])
def add_book(message):
	books_list = {}

	def book_cover(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		book = books_list[message.chat.id]
		if (message.content_type == "photo" and message.photo):
			file_id = message.photo[0].file_id
			file_info = bot.get_file(file_id)
			cover = None
			with requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)) as resp:
				if resp:
					book.cover = MEDIA_ROOT + "%s-%s.jpg" % (message.chat.id, message.photo[0].file_id[:20])
					with open(book.cover, "wb+") as f:
						f.write(resp.content)
		else:
			book.cover = None
		resp = Endpoints.post.book(book)
		reply = "New book (%s) created\nYou can now find it in the list of all books\n/books" % book.name if resp \
			else "Server error occured\nBook (%s) was not created\nTry again later" % book.name

		bot.send_message(message.chat.id, reply, reply_markup=markup)

	def book_publisher(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			try:
				publisher = int(message.text)
				book = books_list[message.chat.id]
				book.publisher = publisher

				msg = bot.send_message(message.chat.id, "Send the book's cover image", reply_markup=markup)
				bot.register_next_step_handler(msg, book_cover)
			except Exception:
				msg = bot.send_message(message.chat.id, "Send the book's publisher id in form of a number", reply_markup=markup)
				bot.register_next_step_handler(msg, book_publisher)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)

	def book_author(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			try:
				author = int(message.text)
				book = books_list[message.chat.id]
				book.author = author

				msg = bot.send_message(message.chat.id, "Send the book's publisher id", reply_markup=markup)
				bot.register_next_step_handler(msg, book_publisher)
			except Exception:
				msg = bot.send_message(message.chat.id, "Send the book's author id in form of a number", reply_markup=markup)
				bot.register_next_step_handler(msg, book_author)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)

	def book_pages(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			try:
				pages = int(message.text)
				book = books_list[message.chat.id]
				book.pages = pages

				msg = bot.send_message(message.chat.id, "Send the book's author id", reply_markup=markup)
				bot.register_next_step_handler(msg, book_author)
			except Exception:
				msg = bot.send_message(message.chat.id, "Send the book's amount of pages in form of a number", reply_markup=markup)
				bot.register_next_step_handler(msg, book_pages)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)

	def book_year(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			try:
				year = int(message.text)
				book = books_list[message.chat.id]
				book.year = year

				msg = bot.send_message(message.chat.id, "Send the book's amount of pages", reply_markup=markup)
				bot.register_next_step_handler(msg, book_pages)
			except Exception:
				msg = bot.send_message(message.chat.id, "Send the book's publish year in correct format of year", reply_markup=markup)
				bot.register_next_step_handler(msg, book_year)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)



	def book_name(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			name = message.text
			book = Models.Book(name)
			books_list[message.chat.id] = book

			msg = bot.send_message(message.chat.id, "Send the book's publish year", reply_markup=markup)
			bot.register_next_step_handler(msg, book_year)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)


	markup = types.ReplyKeyboardRemove(selective=False)
	msg = bot.send_message(message.chat.id, "Send the book's name", reply_markup=markup)
	bot.register_next_step_handler(msg, book_name)


@bot.message_handler(commands=['add_author'])
def add_author(message):
	authors_list = {}

	def auth_photo(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		author = authors_list[message.chat.id]
		if (message.content_type == "photo" and message.photo):
			file_id = message.photo[0].file_id
			file_info = bot.get_file(file_id)
			photo = None
			with requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)) as resp:
				if resp:
					author.photo = MEDIA_ROOT + "%s-%s.jpg" % (message.chat.id, message.photo[0].file_id[:20])
					with open(author.photo, "wb+") as f:
						f.write(resp.content)
		else:
			author.photo = None
		resp = Endpoints.post.author(author)
		reply = "New author (%s) created\nYou can now find him in the list of all authors\n/authors" % author.name if resp \
			else "Server error occured\nAuthor (%s) was not created\nTry again later" % author.name

		bot.send_message(message.chat.id, reply, reply_markup=markup)

	def auth_birth(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			try:
				birth = datetime.strptime(message.text, "%Y-%m-%d")
				author = authors_list[message.chat.id]
				author.birth = birth

				msg = bot.send_message(message.chat.id, "Send the author's photo", reply_markup=markup)
				bot.register_next_step_handler(msg, auth_photo)
			except Exception:
				msg = bot.send_message(message.chat.id, "Send the author's date of birth in correct format: yyyy-mm-dd", reply_markup=markup)
				bot.register_next_step_handler(msg, auth_birth)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)



	def auth_name(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			name = message.text
			author = Models.Author(name)
			authors_list[message.chat.id] = author

			msg = bot.send_message(message.chat.id, "Send the author's date of birth in next format: yyyy-mm-dd", reply_markup=markup)
			bot.register_next_step_handler(msg, auth_birth)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)


	markup = types.ReplyKeyboardRemove(selective=False)
	msg = bot.send_message(message.chat.id, "Send the author's name", reply_markup=markup)
	bot.register_next_step_handler(msg, auth_name)


@bot.message_handler(commands=['add_publisher'])
def add_publisher(message):
	publishers_list = {}

	def pub_notes(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):		
			notes = message.text
			publisher = publishers_list[message.chat.id]
			publisher.notes = notes

			resp = Endpoints.post.publisher(publisher)
			reply = "New publisher (%s; %s) created\nYou can now find it in the list of all publishers\n/publishers" % (publisher.name, publisher.notes) if resp \
				else "Server error occured\nPublisher (%s; %s) was not created\nTry again later" % (publisher.name, publisher.notes)

			a = bot.send_message(message.chat.id, reply, reply_markup=markup)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)

	def pub_name(message):
		markup = types.ReplyKeyboardRemove(selective=False)
		if (message.content_type == "text"):
			name = message.text
			publisher = Models.Publisher(name)
			publishers_list[message.chat.id] = publisher

			msg = bot.send_message(message.chat.id, "Send the publisher's notes", reply_markup=markup)
			bot.register_next_step_handler(msg, pub_notes)
		else:
			bot.send_message(message.chat.id, "Text format required", reply_markup=markup)

	markup = types.ReplyKeyboardRemove(selective=False)
	msg = bot.send_message(message.chat.id, "Send the publisher's name", reply_markup=markup)
	bot.register_next_step_handler(msg, pub_name)




bot.polling(none_stop = True)
