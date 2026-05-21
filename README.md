![PyPI - Downloads](https://img.shields.io/pypi/dw/spotipyfree) ![Downloads](https://static.pepy.tech/badge/spotipyfree)
# SpotipyFree

A lightweight **drop-in replacement for Spotipy** without using the spotify api. This project was build because spotify removed access to its API for non-premium users. This project doesn't use ANY Spotify APIs. 
- - -

## Features

*   Drop-in style response compatible with `spotipy`

*   No Spotify account required

*   Returns playback data structured like the official Spotify API


- - -

## Current Status

This project is **experimental**.

Currently implemented:

*   `search()`
*   `track()`  
*   `playlist()`
*   `playlist_items()`
*   `artist()`
*   `artist_albums()`
*   `album()`
*   `album_tracks()`
*   `current_user_recently_played()` - must first run startRecentlyPlayedListener
*   `current_user_saved_tracks()`
*   `me()`
- - -

## Installation

Bash

`pip install spotipyFree`

- - -

## Usage without login

```python
from SpotipyFree import Spotify

sp = Spotify()

search = sp.search("Blinding Light - Weekend")
artist = sp.artist("3Bd1cgCjtCI32PYvDC3ynO")
artistAlbums = sp.artist_albums("3Bd1cgCjtCI32PYvDC3ynO", include_groups="album,single,compilation")
playlist = sp.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
track = sp.track("67Hna13dNDkZvBpTXRIaOJ")
album = sp.album("4m2880jivSbbyEGAKfITCa")
albumTracks = sp.album_tracks("4m2880jivSbbyEGAKfITCa")
```

## Usage with login
```python
sp = Spotify()
sp.login()

status = spotapi.player.PlayerStatus(sp.user_auth)
sp.startRecentlyPlayedListener()
state = status.state.__dict__
saved = sp.current_user_saved_tracks()
me = sp.me()
```

This project is in no way **affiliated with Spotify**.
