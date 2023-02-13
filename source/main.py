#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from media import *
from media_database import *
from media_sources import *
from media_controller import *
from bot_controller import *

import asyncio
import os

def main():
    state_database = StateDatabase('state.db')
    playlist_database = PlaylistDatabase('playlists.db')
    media_controller = MediaController(state_database, MEDIA_PLAYER_TYPES)
    bot_controller = BotController(media_controller, BOT_TYPES)

    request = 'https://youtu.be/pVRSUMC1rjY?list=PL3wd-xTJHxKQ8VCVy0i3wsN4tngNaDV7y'
    request_dictionary = media_controller.get_request_dictionary(request)
    media_controller.insert_request_dictionary(request_dictionary)

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
    main()
