import os
import re
import logging
import requests
import validators

from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)
bot = None

another_content = ['animation', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location',
				 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
                 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                 'migrate_from_chat_id', 'pinned_message']

# handlers
async def process_command_start(message: types.Message):

	message_text = ('🔥<b>Добро пожаловать в Reduce Link Bot!</b>🔥\n\n'
					'Здесь Вы сможете сократить любую ссылку\n'
					'Всё просто: вставляете ссылку в поле для ввода и получаете короткий URL\n\n'
					'Это не все! Бот также умеет расшифровывать короткие ссылки\n'
					'Просто пришли ссылку, и он выведет все перенаправления')

	await message.answer(message_text)

async def process_link_creation(message: types.Message):

	pattern_URL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
	URLS = [url for url in re.findall(pattern_URL, message.text) if url.rstrip()]

	for text in URLS:

		if validators.url(text):

			URL = requests.get("https://clck.ru/--?url=" + text)

			if text != URL.text:
				await message.answer(f'{text} ===> {URL.text}', disable_web_page_preview=True)
			else:

				try:
					URL = requests.get(URL.text)
					link_list = ''
					el = ''
					for num, elem in enumerate(URL.history, 1):
						link_list += str(num) + '. ' + elem.url + '\n'
						el = elem.url
					link_list = f'{text} ===> {el}\n\n' + link_list	
					await message.answer(link_list, disable_web_page_preview=True)
				except:
					await message.answer(f'{text} ===> Что-то пошло не так...')	
		else:
			await message.answer(f'{text} ===> Введите корректную ссылку, содержащую протокол HTTPS(HTTP)')
	
async def send_erray_message(message: types.Message):

	await message.answer('Я поддерживую только текстовые сообщения')

# Selectel Lambda funcs
async def register_handlers(dp: Dispatcher):

	dp.register_message_handler(process_command_start, commands=['start'])
	dp.register_message_handler(send_erray_message, content_types=another_content)
	dp.register_message_handler(process_link_creation)

async def process_event(update, dp: Dispatcher):

	Bot.set_current(dp.bot)
	await dp.process_update(update)

# Selectel serverless entry point
async def main(**kwargs):

	global bot
	bot = Bot(os.environ.get("TOKEN"), parse_mode=types.ParseMode.HTML)
	dp = Dispatcher(bot)

	await register_handlers(dp)

	update = types.Update.to_object(kwargs)
	await process_event(update, dp)

	return 'ok'