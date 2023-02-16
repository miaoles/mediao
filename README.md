# mediao

>02/15/23 - onward this will likely be rewritten around UNIX socket IPC

generates media queues/playlist databases, controls simultaneous playback/interaction for supported media services/interfaces/media players 

example usecase: mpv player, twitch bot interface, 2 media queues: requests queue prioritized, backup queue using generated/imported YouTube/Bandcamp links/playlists

thanks to 

##### initial todo
- services:
  - YouTube ( parsing 🗹, api 🗹, importing 🚧 )
  - Bandcamp ( parsing, importing )
  - localhost ( parsing, importing )
- media players:
  - mpv ( python-mpv 🗹 )
  - PySide ( mpv embed ) ❔
  - web ❔
- interfaces:
  - Twitch chatbot ( pyTwitchAPI 🗹 )
  - cli
  - PySide ❔
- looking into:
  - ipc sockets refactor
  - setup.py
  - toml configuration ❔
  - concurrency/parallelism approach
  - media data approach
  - database approach
  - refactor with nim ❔ ( likely not )
