import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
#from aiohttp import web
#import ssl
import requests

from bot_config import *
from bookstore_api import *



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"This message will help you get along with current bot\nList of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint", reply_markup=markup)
	

@bot.message_handler(commands=['help'])
def send_help(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"List of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint", reply_markup=markup)




def query_markup():
	markup = InlineKeyboardMarkup()
	markup.row_width = 3
	markup.add(
		InlineKeyboardButton("Prev", callback_data="prev_page"),
		InlineKeyboardButton("Close", callback_data="close"),
		InlineKeyboardButton("Next", callback_data="next_page"))
	return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	if call.data == "close":
		pass
	if call.data == "prev_page":
		pass
	elif call.data == "next_page":
		pass

@bot.message_handler(commands=['books'])
def list_books(message):
	books_query = "No books available right now"
	url = bookstore_endpoints.books
	resp = requests.get(url=url, params="{'format':'api'}")
	if (resp):
		books_query = ''
	"""	for book in resp.json():
			books_query = books_query + book.get('name') + ('  (' + str(book.get('year')) + ' year)'if book.get('year') else '')  + '\n'"""
	bot.send_message(message.chat.id, books_query, reply_markup=query_markup())



bot.polling(none_stop = True)

