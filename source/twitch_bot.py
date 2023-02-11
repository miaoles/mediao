#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media_services import *
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
	async def media_request(self, command:ChatCommand):
		media_id = get_media_id(command.parameter)
		if media_id == "None":
			await command.reply(f"Error: Your URL could not be parsed.")
		else:
			await command.reply(f"Success: Your URL was parsed.")

	async def start(self):
		print(f"Starting Twitch Bot.")
		# set up twitch api instance and add user authentication with some scopes
		self.twitch = await Twitch(self.app_id, self.app_secret)
		twitch_authenticator = UserAuthenticator(self.twitch, TWITCH_USER_SCOPE)
		twitch_token, twitch_refresh_token = await twitch_authenticator.authenticate()
		await self.twitch.set_user_authentication(twitch_token, TWITCH_USER_SCOPE, twitch_refresh_token)

		# create chat instance
		self.twitch_chat = await Chat(self.twitch)

		# listen to when the bot is done starting up and ready to join channels
		self.twitch_chat.register_event(ChatEvent.READY, self.on_ready)

		# listen to chat messages
		self.twitch_chat.register_event(ChatEvent.MESSAGE, self.on_message)

		# Commands Registration
		self.twitch_chat.register_command('mediarequest', self.media_request)
		self.twitch_chat.register_command('request', self.media_request)
		self.twitch_chat.register_command('mr', self.media_request)
		self.twitch_chat.register_command('r', self.media_request)

		# we are done with our setup, lets start this bot up!
		self.twitch_chat.start()

	async def stop(self):
		self.twitch_chat.stop()
		await self.twitch.close()
		print(f"Stopped Twitch Bot.")
