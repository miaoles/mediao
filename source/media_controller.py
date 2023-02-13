#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media_database import *
from mpv_player import *

import asyncio


class MediaController:
	def __init__(self, state_database:StateDatabase, media_player_types):
		self.current_media = None
		self.playback_active = False
		self.state_database = state_database
		self.media_players = []
		for media_player_type in media_player_types:
			match media_player_type.casefold():
				case 'mpv':
					self.mpv_player = MPV()
					self.media_players.append(self.mpv_player)
				case _:
					print(f"Could not add player type: {media_player_type}")
		# self.start_media_players()
		# self.enable_playback()
		# asyncio.run(self.enable_playback())

	def start_media_players(self):
		print(f"Starting media players:")
		for media_player in self.media_players:
			print(f"{media_player}")
			asyncio.run(media_player.start())
			media_player.client.observe_property('idle-active',self.idle_event_observed)
		self.initialize_playback()

	def stop_media_players(self):
		print(f"Stopping media players:")
		for media_player in self.media_players:
			print(f"{media_player}")
			asyncio.run(media_player.stop())

	def is_queue_empty(self) -> bool:
		request_queue_is_empty = self.state_database.is_table_empty('request_queue')
		generated_queue_is_empty = self.state_database.is_table_empty('generated_queue')
		if request_queue_is_empty and generated_queue_is_empty:
			print(f"Media not in queue.")
			return True
		else:
			print(f"Media in queue.")
			return False

	def get_request_dictionary(self, media_query:str) -> dict:
		try:
			media_id = get_media_id(media_query)
		except Exception:
			print(f"Media request query failed.")
			raise Exception
		else:
			print(f"Media request query succeeded.")
			youtube_media_dictionary = get_youtube_media_dictionary(media_id)
			media_dictionary = convert_youtube_dictionary(youtube_media_dictionary)
			return media_dictionary

	def insert_request_dictionary(self, media_dictionary:dict):
		try:
			self.state_database.insert_media_dictionary(media_dictionary, 'request_queue')
		except Exception:
			print(f"Media request insert failed.")
			raise Exception
		else:
			print(media_dictionary)

	def set_current_media(self, media:dict):
		self.current_media = media

	def get_current_media(self) -> dict:
		return self.current_media

	def evaluate_media(self):
		pass

	def get_next_media(self) -> dict:
		# This one is gonna have the most customization, but is currently hardcoded.
		request_queue_is_empty = self.state_database.is_table_empty('request_queue')
		# print(f"Request Queue is empty: {request_queue_is_empty}")
		generated_queue_is_empty = self.state_database.is_table_empty('generated_queue')
		# print(f"Generated Queue is empty: {generated_queue_is_empty}")
		if not request_queue_is_empty:
			print(f"Getting media from Request Queue.")
			return self.state_database.get_lowest_id_row('request_queue')
		if not generated_queue_is_empty:
			print(f"Getting media from Generated Queue.")
			return self.state_database.get_lowest_id_row('generated_queue')

	def play_media(self, media:dict):
		print(f"Playing media.")
		for media_player in self.media_players:
			# print(media)
			# media_player.play(media['media_url'])
			media_player.play(media['media_url'])

	def enable_playback(self):
		print(f"Enabling media playback.")
		self.playback_active = True

	def disable_playback(self):
		print(f"Disabling media playback.")
		self.playback_active = False

	def iterate_playback(self):
		next_media = self.get_next_media()
		# print(next_media)
		self.set_current_media(next_media)
		self.play_media(self.get_current_media())

	def initialize_playback(self):
		print(f"Initializing media playback.")
		self.enable_playback()
		self.iterate_playback()

	def idle_event_observed(self, property_name:str, idle:bool):
		if idle and self.playback_active:
			queue_is_empty = self.is_queue_empty()
			if queue_is_empty:
				self.disable_playback()
			if not queue_is_empty:
				self.iterate_playback()
