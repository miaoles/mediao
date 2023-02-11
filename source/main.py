#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media import *
from media_database import *
from media_services import *
from media_controller import *
from bot_controller import *

import asyncio
import os

def main():
    print(os.path.realpath(__file__))

    state_database = StateDatabase('state.db')
    playlist_database = PlaylistDatabase('playlists.db')
    media_controller = MediaController(state_database, MEDIA_PLAYER_TYPES)
    youtube = YouTube(YOUTUBE_API_KEY)
    bot_controller = BotController(media_controller, BOT_TYPES)

    item = {
        'row_id': None,
        'media_id': 'u0dXVZ939Sg',
        'media_url': 'https://youtu.be/VMWorlKKTSA',
        'media_title': 'ヤプーズ ｢私の中の他人｣【ヤプーズ・デ・ラ・クルスの犯罪的人生, 11】',
        'media_service': 'YouTube',
        'media_duration': 'PT3M34S',
        'channel_id': 'UC4w4WOisSjbeZDNb58LN3yQ',
        'channel_title': 'iao',
        'playlist_id': None,
        'playlist_title': None,
        'requester_name': 'requester' }
    item2 = {
        'row_id': None,
        'media_id': 'u0dXVZ939Sg',
        'media_url': 'https://youtu.be/VMWorlKKTSA',
        'media_title': 'ヤプーズ ｢私の中の他人｣【ヤプーズ・デ・ラ・クルスの犯罪的人生, 11】',
        'media_service': 'YouTube',
        'media_duration': 'PT3M34S',
        'channel_id': 'UC4w4WOisSjbeZDNb58LN3yQ',
        'channel_title': 'iao',
        'playlist_id': None,
        'playlist_title': None,
        'requester_name': 'requester' }

    state_database.insert_media_row(item, 'request_queue')
    state_database.insert_media_row(item2, 'generated_queue')

    media_controller.start_media_players()
    # asyncio.run(media_controller.start_media_players())
    bot_controller.start_bots()
    # asyncio.run(bot_controller.start_bots())

    try:
        input(f"Press enter to stop Mediao.\n")
    finally:
        bot_controller.stop_bots()
        media_controller.stop_media_players()


if __name__ == "__main__":
    # asyncio.run(main())
    main()
