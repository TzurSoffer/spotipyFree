# Usage guide

Create a client with `from spotipyfree import Spotify`. A client can be used
without login for selected catalog queries. Methods that access personal
account data or control playback need an authenticated session; see
[Authentication](authentication.md).

## Catalog lookups

Methods accept Spotify IDs, and several also accept Spotify URLs:

```python
spotify.search("artist or track name")
spotify.track("TRACK_ID")
spotify.album("ALBUM_ID")
spotify.album_tracks("ALBUM_ID")
spotify.artist("ARTIST_ID")
spotify.artist_albums("ARTIST_ID", include_groups="album,single")
spotify.playlist("PLAYLIST_ID")
spotify.playlist_items("PLAYLIST_ID")
```

`search()` finds tracks and returns a dictionary with a `"tracks"` collection.
Use the [supported methods](api-reference.md) as a reference for available
catalog lookups.

## Account data

After authenticating, you can read account information such as:

```python
spotify.me()                         # also available as current_user()
spotify.current_user_saved_tracks()
spotify.current_user_saved_tracks_contains(["TRACK_ID"])
spotify.current_user_playlists()
spotify.current_playback()
```

Authentication and session files are described in the
[authentication guide](authentication.md). Protect session data as you would
protect a password.

## Playback controls

The client exposes a small set of basic controls:

```python
spotify.start_playback()
spotify.pause_playback()
spotify.next_track()
spotify.previous_track()
spotify.seek_track(position_ms=30_000)
```

These operations act on the authenticated user's active player session.

## Recently played listener

`current_user_recently_played()` returns the tracks collected in the current
client's in-memory buffer; it is not a direct historical-playback query. Start
the listener first:

```python
spotify.startRecentlyPlayedListener(refreshInterval=3)
recent = spotify.current_user_recently_played()
```

The listener requires authentication and polls player state. The buffer holds
up to 50 entries and is available for the lifetime of the client process.

## Response compatibility

Responses use familiar dictionary structures. See the
[supported methods](api-reference.md) for the data returned by each feature.
