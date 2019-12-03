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
	itembtn4 = types.KeyboardButton('test more')
	markup.add(itembtn1)
	bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
	#bot.reply_to(message, 'Bot started, type /help to get additional help.')

bot.polling(none_stop = True)

