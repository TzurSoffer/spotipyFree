# Legal, privacy, and safety considerations

SpotipyFree is an independent project and is not affiliated with, endorsed by,
or sponsored by Spotify. Spotify features and content are subject to Spotify's
terms and other applicable rules.

Before using this project, review the current terms and policies that apply to
your account, location, and use case. You are responsible for deciding whether
your use is permitted. This documentation is not legal advice.

## Account and privacy

Authenticated features rely on session data. Session cookies are sensitive
credentials. Keep them private, restrict file access, and do not include them
in repositories, logs, screenshots, support requests, or public deployments.
Use account access only where you have authorization.

Some optional lookups use third-party services. Be mindful that query values
and identifiers may be sent to those services; avoid sending private or
personal data.

## HTTP server

The optional Flask server has no authentication and dynamically exposes client
methods. Run it only on loopback in a trusted local environment. Do not make it
publicly reachable.

## Licensing

SpotipyFree is distributed under the MIT License; see the repository's
[LICENSE](https://github.com/TzurSoffer/spotipyFree/blob/main/LICENSE).
This does not grant rights to Spotify content, Spotify marks, or third-party
services.
