#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

# Not used

class Media():
	__slots__ = [
		'row_id',
		'media_id',
		'media_url',
		'media_title',
		'media_source',
		'media_duration',
		'channel_title',
		'playlist_id',
		'playlist_title',
		'requester_name',
		'origin_table' ]

	def __init__(self):
		self.row_id = row_id
		self.media_id = media_id
		self.media_url = media_url
		self.media_title = media_title
		self.media_source = media_source
		self.media_duration = media_duration
		self.channel_title = channel_title
		self.playlist_id = playlist_id
		self.playlist_title = playlist_title
		self.requester_name = requester_name
		self.origin_table = origin_table

# class Media(dict):
# 	def __init__(self):
# 		self['row_id'] = None
# 		self['media_id'] = None
# 		self['media_url'] = None
# 		self['media_title'] = None
# 		self['media_service'] = None
# 		self['media_duration'] = None
# 		self['channel_id'] = None
# 		self['channel_title'] = None
# 		self['playlist_id'] = None
# 		self['playlist_title'] = None
# 		self['requester_name'] = None
