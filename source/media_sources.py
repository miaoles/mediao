#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from enum import Enum, auto
from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse


class MediaSources(Enum):
	YOUTUBE = auto()
	BANDCAMP = auto()
	LOCAL = auto()


def get_media_id(media_url:str) -> str:
	query = urlparse(media_url)
	match query.hostname:
		case 'youtu.be':
			return query.path[1:]
		case  'www.youtube.com' | 'youtube.com' | 'music.youtube.com':
			if query.path[:7] == '/watch/':
				return query.path.split('/')[1]
			if query.path == '/watch':
				return parse_qs(query.query)['v']
			if query.path[:7] == '/embed/':
				return query.path.split('/')[2]
			if query.path[:3] == '/v/':
				return query.path.split('/')[2]
			if query.path[:8] == '/shorts/':
				return query.path.split('/')[2]
		case 'bandcamp.com':
			raise Exception("URL could not be parsed. Bandcamp not supported yet.")
		case _:
			raise Exception("URL could not be parsed.")


# Uses 1 YouTube API Quota Point
def get_youtube_media_dictionary(youtube_media_id: str):
	youtube = build(
		'youtube',
		'v3',
		developerKey=YOUTUBE_API_KEY)
	request = youtube.videos().list(
		part='snippet, contentDetails',
		id=youtube_media_id)
	result = request.execute()
	return result


def convert_youtube_dictionary(youtube_dictionary) -> dict:
	media_dictionary = {
		'media_id': youtube_dictionary['items'][0]['id'],
		'media_url': 'http://youtu.be/' + youtube_dictionary['items'][0]['id'],
		'media_title': youtube_dictionary['items'][0]['snippet']['title'],
		'media_source': 'YouTube',
		'media_duration': youtube_dictionary['items'][0]['contentDetails']['duration'],
		'channel_title': youtube_dictionary['items'][0]['snippet']['channelTitle'],
		'playlist_id': None,
		'playlist_title': None,
		'requester_name': None,
		'origin_table': None
	}
	return media_dictionary

# try:
# 	url = get_media_id('https://www.youtube.com/watch?v=Ky2JPucaXAw')
# 	print(url)
# 	# parse_media_url('cock')
# except:
# 	print(f"oops")
	# media['items'][0]['url'] = "http://youtu.be/" + youtube_dictionary['items'][0]['id']

	# class YouTube:
	# def __init__(self, api_key:str):
	# 	self.api_key = api_key
 #
	# # Uses 1 YouTube API Quota Point
	# def get_media_dictionary(self, youtube_media_id: str):
	# 	youtube = build(
	# 		'youtube',
	# 		'v3',
	# 		developerKey=self.api_key)
	# 	request = youtube.videos().list(
	# 		part='snippet, contentDetails',
	# 		id=youtube_media_id)
	# 	result = request.execute()
	# 	return result
