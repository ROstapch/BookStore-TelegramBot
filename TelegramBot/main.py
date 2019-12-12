import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
#from aiohttp import web
#import ssl

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




def query_markup(response=None):
	markup = InlineKeyboardMarkup()

	if (response and response.ok):
		temp = KeyboardRow()
		for i in range(0, response.on_page):
			temp.add(InlineKeyboardButton(str(i + 1), callback_data=str(i + 1)))
			if ((i + 1) % 5 == 0):
				markup.row(*temp.keyboard)
				temp = KeyboardRow()
		markup.row(*temp.keyboard)

		temp = KeyboardRow()
		if (response.prev_page):
			temp.add(InlineKeyboardButton("Prev", callback_data="prev_page"))
		temp.add(InlineKeyboardButton("Close", callback_data="close"))
		if (response.next_page):
			temp.add(InlineKeyboardButton("Next", callback_data="next_page"))
		markup.row(*temp.keyboard)
	return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	if call.data == "close":
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	else:
		reply_call = CallbackHandle.query(call)
		if call.data == "1":
			pass
		if call.data == "2":
			pass
		if call.data == "3":
			pass
		if call.data == "4":
			pass
		if call.data == "5":
			pass
		if call.data == "6":
			pass
		if call.data == "7":
			pass
		if call.data == "8":
			pass
		if call.data == "9":
			pass
		if call.data == "10":
			pass

		elif call.data == "prev_page":
			if(reply_call.prev_page):
				resp_parsed = get_page(reply_call.prev_page, reply_call.query_type)
				bot.edit_message_text(text=resp_parsed.reply, chat_id=call.message.chat.id,
					message_id=call.message.message_id, inline_message_id=call.inline_message_id,
					reply_markup=query_markup(resp_parsed))

		elif call.data == "next_page":
			if(reply_call.next_page):
				resp_parsed = get_page(reply_call.next_page, reply_call.query_type)
				bot.edit_message_text(text=resp_parsed.reply, chat_id=call.message.chat.id,
					message_id=call.message.message_id, inline_message_id=call.inline_message_id,
					reply_markup=query_markup(resp_parsed))


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



bot.polling(none_stop = True)

