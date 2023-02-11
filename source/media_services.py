#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from googleapiclient.discovery import build

from urllib.parse import parse_qs, urlparse


class YouTube:
	def __init__(self, api_key:str):
		self.api_key = api_key

	# Uses 1 YouTube API Quota Point
	def get_media_information(self, youtube_media_id: str):
		youtube = build(
			'youtube',
			'v3',
			developerKey=self.api_key)
		request = youtube.videos().list(
			part='snippet, contentDetails',
			id=youtube_media_id)
		result = request.execute()
		return result


def get_media_id(media_url:str) -> str:
	query = urlparse(media_url)
	if query.hostname == 'youtu.be':
		return query.path[1:]
	if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
		if query.path[:7] == '/watch/':
			return query.path.split('/')[1]
		if query.path == '/watch':
			return parse_qs(query.query)['v'][0]
		if query.path[:7] == '/embed/':
			return query.path.split('/')[2]
		if query.path[:3] == '/v/':
			return query.path.split('/')[2]
		if query.path[:8] == '/shorts/':
			return query.path.split('/')[2]
	if query.hostname == 'bandcamp.com':
		print(f"Bandcamp not supported yet.")
		return None
	return None # if the ifs failed


def get_media_dictionary(media_id:str) -> dict:
	pass
