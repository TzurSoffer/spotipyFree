# What is SpotipyFree?

SpotipyFree is a Python library that makes Spotify catalog, account, and
playback features available through a familiar Spotipy-style interface. It was built because spotify removed access to its API for non-premium users. It aims to make the spotify api as easy and frictionless to use. Migration from spotipy is super straightforward, in most cases only requiring you to change the import name. The project also aims to provide a straightforward user experience for new users trying to get started.

## What it does

- Search for tracks and retrieve track, album, artist, and playlist details.
- Browse album tracks, artist discographies, and playlist tracks.
- Read saved tracks, saved-track membership, playlists, profile, and playback
  state with an authenticated account.
- Control playback with play, pause, next, previous, and seek commands.
- Collect recently played tracks while the listener is running.
- Use an optional local Flask interface to call client methods over HTTP.

See the [supported methods](api-reference.md), [usage guide](usage.md), and
[quick start](quickstart.md) for examples.
