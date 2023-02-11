# mediao

(experimental, proof of concept)

generates media queues/playlist databases, controls simultaneous playback/interaction for supported media services/interfaces/media players 

example usecase: mpv player, twitch bot interface, 2 media queues: requests queue prioritized, backup queue using generated/imported YouTube/Bandcamp links/playlists

##### initial todo
- services:
  - YouTube (parsing 🗹, api 🗹, importing 🚧)
  - Bandcamp (parsing, importing)
  - localhost (parsing, importing)
- media players:
  - mpv 🗹
  - PySide (mpv embed) ❔
  - web ❔
- interfaces:
  - Twitch chatbot 🗹
  - cli
  - PySide ❔
- looking into:
  - setup.py
  - concurrency/parallelism approach
  - media data approach
  - database approach
  - pipes ❔
  - possible refactor to nim (likely not)
