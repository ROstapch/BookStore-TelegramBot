import telebot
from telebot import types
from aiohttp import web
import ssl

from bot_config import *



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	itembtn1 = types.KeyboardButton('Books')
	itembtn2 = types.KeyboardButton('Authors')
	itembtn3 = types.KeyboardButton('Publishers')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
	

@bot.message_handler(commands=['help'])
def send_help(message):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(message.chat.id,
		"This message is to help you get along with current bot\nList of all commands:\n\n"+
		"/start - to start the bot\n"+
		"/help - to show this hint", reply_markup=markup)


bot.polling(none_stop = True)

