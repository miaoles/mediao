#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *
from file_path import *
from database import *

import sqlite3
from sqlite3 import Error


class MediaDatabase(Database):
	def create_media_table(self, table_name:str):
		self.delete_table(table_name)
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS " +
			table_name +
				"(row_id  INTEGER PRIMARY KEY AUTOINCREMENT," +
				"media_id TEXT," +
				"media_url TEXT," +
				"media_title TEXT," +
				"media_service TEXT," +
				"media_duration TEXT," +
				"channel_id TEXT," +
				"channel_title TEXT," +
				"playlist_id TEXT," +
				"playlist_title TEXT," +
				"requester_name TEXT)")
		self.connection.commit()

	def insert_media_row(self, media:dict, table_name:str):
		media = media
		self.cursor.execute(
			"INSERT INTO " +
			table_name +
			" (row_id, media_id, media_url, media_title, media_service, media_duration, " +
			"channel_id, channel_title, playlist_id, playlist_title, requester_name) " +
			"VALUES (NULL,:media_id, :media_url, :media_title, :media_service, :media_duration, " +
			":channel_id, :channel_title, :playlist_id, :playlist_title, :requester_name)",
			media)
		self.connection.commit()
		# self.read_table(table_name)


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
