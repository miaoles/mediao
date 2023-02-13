#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *
from file_path import *

import time
import os
from threading import Lock
import sqlite3
from sqlite3 import Error


class Database:
	def __init__(self,database_name:str):
		self.set_database_path(database_name)
		self.establish_database_connection()
		self.initialize_database_tables()

	def set_database_path(self,database_name:str):
		self.database_path = get_current_file_path() + '/databases/' + database_name

	def establish_database_connection(self):
		print(f"Connecting to database: {self.database_path}")
		self.connection = sqlite3.connect(self.database_path, check_same_thread=False)
		self.connection.row_factory = self.dictionary_factory
		self.cursor = self.connection.cursor()
		self.lock = Lock()

	def connection_commit(self):
		self.connection.commit()

	def initialize_database_tables(self):
		pass

	def dictionary_factory(self, cursor, row) -> dict:
		fields = [column[0] for column in cursor.description]
		return {key: value for key, value in zip(fields, row)}

	def is_table_empty(self, table_name:str) -> bool:
		self.lock.acquire(True)
		self.cursor.execute(
			"SELECT COUNT(1) WHERE EXISTS (SELECT 1 FROM " +
			table_name + ")")
		result = self.cursor.fetchone()
		self.lock.release()
		self.connection_commit()
		if result['COUNT(1)'] > 0:
			return False
		else:
			return True

	def delete_table(self, table_name:str):
		self.lock.acquire(True)
		self.cursor.execute(
			"DROP TABLE IF EXISTS " +
			table_name)
		self.lock.release()
		self.connection_commit()

	def get_lowest_id_row(self, table_name:str) -> dict:
		self.lock.acquire(True)
		self.cursor.execute(
			"SELECT * FROM " +
			table_name +
			" LIMIT 1")
		row = self.cursor.fetchone()
		self.lock.release()
		self.connection_commit()
		return row

	def delete_lowest_id_row(self, table_name:str):
		self.lock.acquire(True)
		self.cursor.execute(
			"DELETE FROM "+
			table_name +
			" WHERE row_id = (SELECT min(row_id) FROM " +
			table_name + ")")
		self.lock.release()
		self.connection_commit()

	def read_table(self, table_name:str):
		self.lock.acquire(True)
		self.cursor.execute("SELECT * FROM " + table_name)
		rows = self.cursor.fetchall()
		self.lock.release()
		self.connection_commit()
		print(f"{rows}")
