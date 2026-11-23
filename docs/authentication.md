# Authentication and session data

Catalog lookups such as track, album, artist, playlist, and search operations
are intended to work without signing in. Personal account data and playback
operations use an authenticated session.

## Sign in

The client can attempt to load a session when it is created or when `login()`
is called:

```python
from spotipyfree import Spotify

spotify = Spotify()
if not spotify.login():
    raise RuntimeError("Could not load a SpotipyFree session")
```

By default, the client looks for a session file in its configuration
directory. The client can guide you through importing a session when one is
not already available. You can also provide a `cookiesFile` path:

```python
spotify = Spotify(cookiesFile="path/to/session.json")
```

Use `login()` to load an existing account session.

## Session file location

SpotipyFree's default cookie file is `cookies.json` under its configuration
directory:

- Linux: `~/.config/spotipyFree/cookies.json`
- Windows and other platforms: `~/.spotipyFree/cookies.json`

The `getConfigFolder()` and `getCookiesFile()` helpers are also exported by the
package.

## Protect your session

Browser session cookies are bearer credentials: anyone who obtains them may be
able to access the associated account. Never paste them into source code,
commit them, upload them to issue trackers, or send them to third parties.
Restrict access to the session file and revoke sessions if you suspect they
were exposed. Do not deploy cookie-based account access in a shared or
untrusted environment.

For legal and service-policy considerations, see
[Legal and safety](legal-and-safety.md).
