# Troubleshooting

## `ModuleNotFoundError` when importing SpotipyFree

Install the package in the Python environment running your script:

```bash
python -m pip install spotipyFree
python -c "from spotipyfree import Spotify; print(Spotify)"
```

Both `from spotipyfree import Spotify` and the existing
`from SpotipyFree import Spotify` spelling are supported.

## A catalog lookup fails

Check your network connection, confirm the Spotify ID or URL, and retry.
Search accepts a query string; track, album, artist, and playlist methods
accept their Spotify ID or link.

## An account method fails

Confirm that the session is valid and that the method is documented as
requiring authentication in the [API reference](api-reference.md). Session
cookies can expire. Never share them when requesting help.

## `current_user_recently_played()` is empty

Call `startRecentlyPlayedListener()` to collect recent track activity, then
read it with `current_user_recently_played()`. The listener collects playback
while it is running; its in-memory buffer starts empty for each process.

## The Flask example cannot import Flask

Install Flask in the same environment as SpotipyFree:

```bash
python -m pip install Flask
```

## Report a reproducible issue

When opening a [GitHub issue](https://github.com/TzurSoffer/spotipyFree/issues),
include the package version, Python version, method name, and a sanitized error
message. Remove cookies, access tokens, personal account details, and other
secrets from logs and code samples.
