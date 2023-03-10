#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

import asyncio
import mpv


class MPV():
	def __init__(self):
		self.window_title=MEDIA_WINDOW_TITLE
		self.window_geometry=MEDIA_WINDOW_GEOMETRY

	async def start(self):
		print(f"Starting MPV Player.")
		self.client = mpv.MPV(
			title=self.window_title,
			geometry=self.window_geometry,
			ytdl=True,
			osc=True,
			player_operation_mode='pseudo-gui',
			script_opts='osc-idlescreen=no,osc-scalewindowed=2.0',
			input_default_bindings=True,
			input_vo_keyboard=True,
			af="loudnorm=I=-24.0:LRA=24.0:TP=-6.0",
			# ytdl-format="bestvideo[height=?144][fps<=?30][vcodec!=?vp9]+bestaudio/best"
			ytdl_format="bestvideo[height<=?480]+bestaudio/best" )
		# self.client.observe_property('idle-active',self.idle_event_observed)

	async def stop(self):
		self.client.terminate()
		print(f"Stopped MPV Player.")

	def play(self,media_url:str):
		self.client.play(media_url)

	# def idle_event_observed(self, property_name, property_value):
	# 	print(f"Idle status changed: {property_value}")
