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
- - -

## Installation

Bash

`pip install spotipyFree`

- - -

## Usage

```python
from SpotipyFree import Spotify

sp = Spotify()
search = sp.search("Blinding Light - Weekend")
playlist = sp.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
track = sp.track("67Hna13dNDkZvBpTXRIaOJ")
album = sp.album("4m2880jivSbbyEGAKfITCa")
albumTracks = sp.album_tracks("4m2880jivSbbyEGAKfITCa")
```


This project is in no way **affiliated with Spotify**.
