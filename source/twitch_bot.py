#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media_controller import *

from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand


TWITCH_USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


class TwitchBot():
	def __init__(self, media_controller:MediaController, app_id, app_secret, target_channel):
		self.media_controller = media_controller
		self.app_id = app_id
		self.app_secret = app_secret
		self.target_channel = target_channel

	# called when the event READY is triggered, which will be on bot start
	async def on_ready(self, ready_event:EventData):
		print(f"Twitch Bot is ready.")
		await ready_event.chat.join_room(self.target_channel)

	async def on_message(self, message:ChatMessage):
		print(f'[#{message.room.name}] {message.user.name}: {message.text}')

	# !mediarequest command
	async def request_media_insert(self, command:ChatCommand):
		try:
			media = self.media_controller.get_request_dict(command.parameter)
		except Exception:
			await command.reply(f"Error: Your URL could not be parsed.")
		else:
			self.media_controller.insert_request_dict(media)
			await command.reply(f"Success: '{media['media_title']}' from ''{media['channel_title']}' was requested.")

	async def request_media_import(self, command:ChatCommand):
		if command.user.name == "iao_":
			await command.reply(f"Importing...")
			self.media_controller.insert_request_playlist(command.parameter)
		else:
			await command.reply(f"Error: You are not permitted to command this.")
		# try:
		# 	media = self.media_controller.get_request_dict(command.parameter)
		# except Exception:
		# 	await command.reply(f"Error: Your URL could not be parsed.")
		# else:
		# 	self.media_controller.insert_request_dict(media)
		# 	await command.reply(f"Success: '{media['media_title']}' from ''{media['channel_title']}' was requested.")

	# !mediarequest command
	async def request_current_media(self, command:ChatCommand):
		try:
			media = self.media_controller.get_current_media()
		except Exception:
			await command.reply(f"Error: No current media.")
		else:
			await command.reply(f"{media['media_title']}  from {media['channel_title']} requested by {media['requester_name']}. ( {media['media_url']} )")

	async def start(self):
		print(f"Starting Twitch Bot.")
		self.twitch = await Twitch(self.app_id, self.app_secret)
		twitch_authenticator = UserAuthenticator(self.twitch, TWITCH_USER_SCOPE)
		twitch_token, twitch_refresh_token = await twitch_authenticator.authenticate()
		await self.twitch.set_user_authentication(twitch_token, TWITCH_USER_SCOPE, twitch_refresh_token)

		self.twitch_chat = await Chat(self.twitch)
		self.twitch_chat.register_event(ChatEvent.READY, self.on_ready)
		self.twitch_chat.register_event(ChatEvent.MESSAGE, self.on_message)

		# Commands Registration
		for command in ['mediarequest','singlerequest','request','mr','sr','r']:
			self.twitch_chat.register_command(command, self.request_media_insert)
		for command in ['currentmedia','media','cm', 'c']:
			self.twitch_chat.register_command(command, self.request_current_media)
		for command in ['wrongmedia','wrong','wm', 'w']:
			self.twitch_chat.register_command(command, self.request_current_media)
		for command in ['importmedia','import','im', 'i']:
			self.twitch_chat.register_command(command, self.request_media_import)

		self.twitch_chat.start()

	async def stop(self):
		self.twitch_chat.stop()
		await self.twitch.close()
		print(f"Stopped Twitch Bot.")
