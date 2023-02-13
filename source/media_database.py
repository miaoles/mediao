#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from file_path import *
from database import *
from media_sources import *

from enum import Enum
import sqlite3
from sqlite3 import Error


class MediaDatabase(Database):
	def create_media_table(self, table_name:str):
		self.delete_table(table_name)
		self.lock.acquire(True)
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS " +
			table_name +
				"(row_id  INTEGER PRIMARY KEY AUTOINCREMENT," +
				"media_id TEXT," +
				"media_url TEXT," +
				"media_title TEXT," +
				"media_source TEXT," +
				"media_duration TEXT," +
				"channel_title TEXT," +
				"playlist_id TEXT," +
				"playlist_title TEXT," +
				"requester_name TEXT)")
		self.lock.release()
		self.connection.commit()

	def insert_media_dictionary(self, media:dict, table_name:str):
		self.lock.acquire(True)
		self.cursor.execute(
			"INSERT INTO " +
			table_name +
			" (row_id, media_id, media_url, media_title, media_source, media_duration, " +
			" channel_title, playlist_id, playlist_title, requester_name) " +
			"VALUES (NULL,:media_id, :media_url, :media_title, :media_source, :media_duration, " +
			":channel_title, :playlist_id, :playlist_title, :requester_name)",
			media)
		self.lock.release()
		self.connection.commit()

# 	def insert_youtube_dictionary(self, media:dict, table_name:str):
# 		media[0]['url'] = "http://youtu.be/" + media[0]['id']
# 		self.cursor.execute(
# 			"INSERT INTO " +
# 			table_name +
# 			" (row_id, media_id, media_url, media_title, media_source, media_duration, " +
# 			"channel_id, channel_title, playlist_id, playlist_title, requester_name) " +
# 			"VALUES (NULL,:media_id, :media_url, :media_title, :media_source, :media_duration, " +
# 			":channel_id, :channel_title, :playlist_id, :playlist_title, :requester_name)",
#
# 			)
# 		self.connection.commit()

	def insert_youtube_flat_playlist(self, media:dict, table_name:str):
		# self.cursor.execute()
		# self.connection.commit()
		pass


class StateDatabase(MediaDatabase):
	def initialize_database_tables(self):
		self.create_media_table('request_queue')
		self.create_media_table('generated_queue')
		self.create_media_table('history')

	def evaluate_exclusions(self, item):
		pass


class PlaylistDatabase(MediaDatabase):
	def initialize_database_tables(self):
		self.create_media_table('playlist_1')

	def evaluate_exclusions(self, item):
		pass

	def import_media_playlist():
		pass
