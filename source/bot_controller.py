#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media_services import *
from media_controller import *
from twitch_bot import *

import asyncio


class BotController:
	def __init__(self, media_controller:MediaController, bot_types):
		self.bots = []
		for bot_type in bot_types:
			match bot_type.casefold():
				case 'twitch':
					self.twitch_bot = TwitchBot(
						media_controller,
						TWITCH_APP_ID,
						TWITCH_APP_SECRET,
						TWITCH_TARGET_CHANNEL )
					self.bots.append(self.twitch_bot)
				case _:
					print(f"Could not add bot type: {bot_type}.")

	def start_bots(self):
		print(f"Starting bots:")
		for bot in self.bots:
			print(f"{bot}")
			# bot.start()
			asyncio.run(bot.start())

	def stop_bots(self):
		print(f"Stopping bots:")
		for bot in self.bots:
			print(f"{bot}")
			# bot.stop()
			asyncio.run(bot.stop())
