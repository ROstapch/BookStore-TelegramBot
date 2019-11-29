import telebot
from aiohttp import web
import ssl

from bot_config import *



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Bot started, type /help to get additional help.')

bot.polling()

