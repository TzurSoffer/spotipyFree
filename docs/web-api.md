# Optional local web API

SpotipyFree includes `SpotipyFree.web.runWebAPI()`, which creates a Flask
application with POST routes for callable client methods. Flask is optional and
must be installed separately:

```bash
python -m pip install Flask
python -c "import spotipyfree.web as web; web.runWebAPI()"
```

The development server listens on `127.0.0.1:5000` by default. Routes accept a
JSON array of positional arguments. For example, in another Python process:

```python
import requests

response = requests.post(
    "http://127.0.0.1:5000/search",
    json=["Blinding Lights The Weeknd"],
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

For the currently registered method, the body above invokes the equivalent
of `search("Blinding Lights The Weeknd")`.

## Run the server locally

The server is designed for local development:

- Keep it on loopback and use it in a trusted local environment.
- The server does not include authentication or authorization.
- Routes expose the client's public callable methods.

Do not expose the server to untrusted users or the public internet.
