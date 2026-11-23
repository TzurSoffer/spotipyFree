# Quick start

## First example: print a track's details

Create a client, look up a track using its Spotify URL, and print its title,
artists, and length:

```python
from spotipyfree import Spotify

spotify = Spotify()
track = spotify.track(
    "https://open.spotify.com/track/67Hna13dNDkZvBpTXRIaOJ"
)

artists = ", ".join(artist["name"] for artist in track["artists"])
minutes, seconds = divmod(track["duration_ms"] // 1000, 60)

print(f"Name: {track['name']}")
print(f"Artists: {artists}")
print(f"Length: {minutes}:{seconds:02}")
```

## Search and browse catalog data

Some catalog lookups work without logging in:

```python
from spotipyfree import Spotify

spotify = Spotify()
results = spotify.search("Blinding Lights The Weeknd")
for track in results["tracks"]["items"]:
    print(track["name"], "-", ", ".join(a["name"] for a in track["artists"]))

track = spotify.track("67Hna13dNDkZvBpTXRIaOJ")
album = spotify.album("4m2880jivSbbyEGAKfITCa")
artist = spotify.artist("3Bd1cgCjtCI32PYvDC3ynO")
playlist_tracks = spotify.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
```

Provide a Spotify ID or an `open.spotify.com` URL to the track, album, artist,
and playlist lookup methods. Search finds tracks by a query string.

## Use account and playback features

Account features use an authenticated session. See
[Authentication](authentication.md) before calling `login()`.

```python
from spotipyfree import Spotify

spotify = Spotify()
if not spotify.login():
    raise RuntimeError("SpotipyFree could not load an authenticated session")

profile = spotify.me()
saved_tracks = spotify.current_user_saved_tracks()
playback = spotify.current_playback()
```

## Next steps

- Browse the [usage guide](usage.md) for catalog, account, and playback
  operations.
- Browse [examples and real-world uses](api-reference.md) for more examples and
  the full feature list.
- Read [legal and safety considerations](legal-and-safety.md) before using
  authentication or the HTTP server.
