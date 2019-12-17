import telebot
from telebot import types
#from aiohttp import web
#import ssl

from bot_config import *
from bookstore_api import *
from markup import *


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
		"/publishers - get list of all publishers\n", reply_markup=markup)
	

@bot.message_handler(commands=['help'])
def send_help(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"List of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint\n" +
		"/books - get list of all books\n" + 
		"/authors - get list of all authors\n" +
		"/publishers - get list of all publishers\n", reply_markup=markup)


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
	pass


@bot.message_handler(commands=['add_author'])
def add_author(message):
	pass


@bot.message_handler(commands=['add_publisher'])
def add_publisher(message):
	publishers_list = {}

	def pub_notes(message):
		notes = message.text
		publisher = publishers_list[message.chat.id]
		publisher.notes = notes

		resp = Endpoints.post.publisher(publisher)
		reply = "New publisher (%s; %s) created\nYou can now find it in the list of all publishers\n/publishers" % (publisher.name, publisher.notes) if resp \
			else "Server error occured\nPublisher (%s; %s) was not created\nTry again later" % (publisher.name, publisher.notes)

		markup = types.ReplyKeyboardRemove(selective=False)
		a = bot.send_message(message.chat.id, reply, reply_markup=markup)

	def pub_name(message):
		name = message.text
		publisher = Models.Publisher(name)
		publishers_list[message.chat.id] = publisher

		markup = types.ForceReply(selective=False)
		msg = bot.send_message(message.chat.id, "Send the publisher's notes", reply_markup=markup)
		bot.register_next_step_handler(msg, pub_notes)

	markup = types.ForceReply(selective=False)
	msg = bot.send_message(message.chat.id, "Send the publisher's name", reply_markup=markup)
	bot.register_next_step_handler(msg, pub_name)




bot.polling(none_stop = True)
