# Examples and real-world uses

`SpotipyFree.Spotify` provides catalog, account, playback, and recently played
features through a Spotipy-style Python interface. The examples below use the
lowercase import name.

Create a client for catalog examples:

```python
from spotipyfree import Spotify

spotify = Spotify()
```

## Practical examples

These examples show common tasks using the returned data.

### Search and print track names and artists

```python
results = spotify.search("Blinding Lights The Weeknd")

for track in results["tracks"]["items"]:
    artists = ", ".join(artist["name"] for artist in track["artists"])
    print(f"{track['name']} - {artists}")
```

### Get a track by URL and print its name, artists, and length

```python
track_url = "https://open.spotify.com/track/67Hna13dNDkZvBpTXRIaOJ"
track = spotify.track(track_url)

artists = ", ".join(artist["name"] for artist in track["artists"])
minutes, seconds = divmod(track["duration_ms"] // 1000, 60)

print(f"Name: {track['name']}")
print(f"Artists: {artists}")
print(f"Length: {minutes}:{seconds:02}")
print(f"URL: {track['external_urls']['spotify']}")
```

### Print an album's tracks

```python
album_url = "https://open.spotify.com/album/4m2880jivSbbyEGAKfITCa"
album = spotify.album(album_url)
print(f"Album: {album['name']}")

for track in spotify.album_tracks(album_url)["items"]:
    print(f"{track['track_number']}. {track['name']}")
```

### Print tracks from a playlist

```python
playlist_url = "https://open.spotify.com/playlist/6lnfkAgnVtNzvj8KScLSkj"
playlist = spotify.playlist(playlist_url)
print(f"Playlist: {playlist['name']}")

for item in spotify.playlist_items(playlist_url)["items"]:
    track = item["track"]
    artists = ", ".join(artist["name"] for artist in track["artists"])
    print(f"{track['name']} - {artists}")
```

### Read authenticated account and playback data

```python
if not spotify.login():
    raise RuntimeError("Could not load an authenticated session")

profile = spotify.me()
print("Signed in as:", profile["display_name"])

playback = spotify.current_playback()
print("Now playing:", playback["name"])
print("Is playing:", playback["is_playing"])
```

## Supported catalog methods

| Method | Feature | Example |
| --- | --- | --- |
| `search(query)` | Search for tracks. | `spotify.search("Blinding Lights The Weeknd")` |
| `track(trackId)` | Retrieve track details by Spotify ID or link. | `spotify.track("https://open.spotify.com/track/67Hna13dNDkZvBpTXRIaOJ")` |
| `album(albumId)` | Retrieve album details by Spotify ID or link. | `spotify.album("https://open.spotify.com/album/4m2880jivSbbyEGAKfITCa")` |
| `album_tracks(albumId)` | List an album's tracks by Spotify ID or link. | `spotify.album_tracks("4m2880jivSbbyEGAKfITCa")` |
| `artist(artistId)` | Retrieve artist details by Spotify ID or link. | `spotify.artist("https://open.spotify.com/artist/3Bd1cgCjtCI32PYvDC3ynO")` |
| `artist_albums(artistId, include_groups="album")` | Browse an artist's albums by Spotify ID or link. | `spotify.artist_albums("3Bd1cgCjtCI32PYvDC3ynO", include_groups="album,single")` |
| `playlist(playlistId)` | Retrieve playlist details by Spotify ID or link. | `spotify.playlist("https://open.spotify.com/playlist/6lnfkAgnVtNzvj8KScLSkj")` |
| `playlist_items(playlistId)` | List tracks in a playlist by Spotify ID or link. | `spotify.playlist_items("6lnfkAgnVtNzvj8KScLSkj")` |
| `audio_features(trackIds)` | Retrieve audio feature information for one or more tracks. | `spotify.audio_features("67Hna13dNDkZvBpTXRIaOJ")` |

Set `getIsrc=True` when creating a client to request ISRC enrichment for track
data and playlist tracks. Asynchronous playlist enrichment uses `aiohttp`.

## Supported account and playback methods

Create a client and sign in before using account or playback methods:

```python
from spotipyfree import Spotify

spotify = Spotify()
if not spotify.login():
    raise RuntimeError("Could not load an authenticated session")
```

| Method | Description | Example |
| --- | --- | --- |
| `login(cookiesFile=None)` | Load an account session. | `spotify.login()` or `spotify.login(cookiesFile="path/to/cookies.json")` |
| `me()` | Read the authenticated user's profile. | `profile = spotify.me()` |
| `current_user()` | Read the authenticated user's profile. | `profile = spotify.current_user()` |
| `current_user_saved_tracks()` | List saved tracks. | `saved = spotify.current_user_saved_tracks()` |
| `current_user_saved_tracks_contains(tracks)` | Check track IDs against saved tracks. | `contains = spotify.current_user_saved_tracks_contains(["67Hna13dNDkZvBpTXRIaOJ"])` |
| `current_user_playlists()` | Read playlists in the account library. | `playlists = spotify.current_user_playlists()` |
| `current_playback()` | Read current player state. | `playback = spotify.current_playback()` |
| `start_playback()` | Resume the active player. | `spotify.start_playback()` |
| `pause_playback()` | Pause the active player. | `spotify.pause_playback()` |
| `next_track()` | Skip to the next track. | `spotify.next_track()` |
| `previous_track()` | Go to the previous track. | `spotify.previous_track()` |
| `seek_track(position_ms)` | Seek to a position in milliseconds. | `spotify.seek_track(position_ms=30_000)` |
| `startRecentlyPlayedListener(refreshInterval=3)` | Start collecting recently played tracks. | `spotify.startRecentlyPlayedListener(refreshInterval=3)` |
| `current_user_recently_played()` | Read tracks collected by the listener. | `recent = spotify.current_user_recently_played()` |

For example, print the profile, saved tracks, and playback state:

```python
profile = spotify.me()
print(profile["display_name"])

for item in spotify.current_user_saved_tracks()["items"]:
    print(item["track"]["name"])

playback = spotify.current_playback()
print(playback["name"], playback["is_playing"])
```

Recently played tracks are collected while the listener is running:

```python
spotify.startRecentlyPlayedListener()
recent = spotify.current_user_recently_played()
print(f"Collected {len(recent)} recently played tracks")
```

## Package helpers

These helper functions are also available from the lowercase package import:

| Function | Example |
| --- | --- |
| `getConfigFolder()` | `from spotipyfree import getConfigFolder; print(getConfigFolder())` |
| `getCookiesFile()` | `from spotipyfree import getCookiesFile; print(getCookiesFile())` |
