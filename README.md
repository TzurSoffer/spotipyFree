![PyPI - Downloads](https://img.shields.io/pypi/dw/spotipyfree) ![Downloads](https://static.pepy.tech/badge/spotipyfree) [![Documentation](https://img.shields.io/badge/docs-read%20the%20docs-blue)](https://spotipyfree.readthedocs.io/)
# SpotipyFree

A lightweight **drop-in replacement for Spotipy** without using the spotify api. This project was built because spotify removed access to its API for non-premium users. This project doesn't use ANY Spotify APIs.
- - -

## Features

- Search the catalog and retrieve track, album, artist, and playlist data.
- With an authenticated account, inspect saved tracks, playlists, profile, and
  playback state, and issue basic playback controls.
- Optionally expose client methods through a local Flask HTTP server.

Catalog lookups are available without signing in. Account and playback
features use an authenticated session; see the
[examples and real-world uses](https://spotipyfree.readthedocs.io/en/latest/api-reference.html)
and [authentication guide](https://spotipyfree.readthedocs.io/en/latest/authentication.html).

## Install

```bash
python -m pip install spotipyFree
```

Requires Python 3.9 or newer.

## Examples

### Search for tracks

```python
from spotipyfree import Spotify

spotify = Spotify()
results = spotify.search("Blinding Lights The Weeknd")

for track in results["tracks"]["items"]:
    artists = ", ".join(artist["name"] for artist in track["artists"])
    print(f"{track['name']} - {artists}")
```

### Get a track from its Spotify URL

```python
track_url = "https://open.spotify.com/track/67Hna13dNDkZvBpTXRIaOJ"
track = spotify.track(track_url)

artists = ", ".join(artist["name"] for artist in track["artists"])
print(f"Name: {track['name']}")
print(f"Artists: {artists}")
print(f"Duration: {track['duration_ms'] / 1000:.0f} seconds")
print(f"Spotify URL: {track['external_urls']['spotify']}")
```

### Get an album and list its tracks

```python
album_url = "https://open.spotify.com/album/4m2880jivSbbyEGAKfITCa"
album = spotify.album(album_url)
print(f"Album: {album['name']}")
print("Artists:", ", ".join(artist["name"] for artist in album["artists"]))

tracks = spotify.album_tracks(album_url)
for track in tracks["items"]:
    print(f"{track['track_number']}. {track['name']}")
```

### Get an artist and browse their albums

```python
artist_url = "https://open.spotify.com/artist/3Bd1cgCjtCI32PYvDC3ynO"
artist = spotify.artist(artist_url)
print(f"Artist: {artist['name']}")

albums = spotify.artist_albums(artist["id"], include_groups="album,single")
for album in albums["items"]:
    print(album["name"])
```

### Read a playlist

```python
playlist_url = "https://open.spotify.com/playlist/6lnfkAgnVtNzvj8KScLSkj"
playlist = spotify.playlist(playlist_url)
print(f"Playlist: {playlist['name']}")

for item in spotify.playlist_items(playlist_url)["items"]:
    track = item["track"]
    artists = ", ".join(artist["name"] for artist in track["artists"])
    print(f"{track['name']} - {artists}")
```

### Read account and playback information

Account features require an authenticated session. The first login may prompt
you to import a session; see the [authentication guide](https://spotipyfree.readthedocs.io/en/latest/authentication.html).

```python
if not spotify.login():
    raise RuntimeError("Could not load an authenticated session")

print("Signed in as:", spotify.me()["display_name"])

saved_tracks = spotify.current_user_saved_tracks()
for item in saved_tracks["items"]:
    track = item["track"]
    print(track["name"], "-", ", ".join(a["name"] for a in track["artists"]))

playback = spotify.current_playback()
print("Now playing:", playback["item"]["name"])
```

### Control playback

Playback controls act on your authenticated active player:

```python
spotify.pause_playback()
spotify.start_playback()  # Resume
spotify.next_track()
spotify.previous_track()
spotify.seek_track(position_ms=30_000)
```

See the [usage guide](https://spotipyfree.readthedocs.io/en/latest/usage.html)
for more examples.

## Build and preview the documentation

Install the documentation tools and build the HTML site from the repository
root:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W -b html docs build/docs
```

On Windows, the build output is in `build\docs`. Open
`build\docs\index.html` in a browser, or serve it locally:

```bash
python -m http.server 8000 --directory build/docs
```

Then visit `http://localhost:8000`.


## Documentation

- [Read the documentation](https://spotipyfree.readthedocs.io/)
- [Installation and quick start](https://spotipyfree.readthedocs.io/en/latest/installation.html)
- [Usage guides](https://spotipyfree.readthedocs.io/en/latest/usage.html)
- [Examples and real-world uses](https://spotipyfree.readthedocs.io/en/latest/api-reference.html)
- [Legal, privacy, and security considerations](https://spotipyfree.readthedocs.io/en/latest/legal-and-safety.html)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
