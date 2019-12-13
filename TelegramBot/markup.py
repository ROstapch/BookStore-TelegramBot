from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Dictionaryable



class KeyboardRow(Dictionaryable):
	def __init__(self):
		self.keyboard = []

	def add(self, button):
		self.keyboard.append(button)



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


def item_markup():
	markup = InlineKeyboardMarkup()
	markup.row(
		InlineKeyboardButton("Update", callback_data="update_item"),
		InlineKeyboardButton("Close", callback_data="close"),
		InlineKeyboardButton("Delete", callback_data="delete_item"))
	return (markup)

