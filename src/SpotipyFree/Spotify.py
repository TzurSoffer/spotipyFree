import json
import asyncio
import requests
import spotapi  # type: ignore
from collections import deque

try:
    from .utils import getCookiesFile
    from .CookiesExtraction import interactiveMode as extractCookiesFromBrowser
    from .Formatter import SpotifyFormatter
    from .LastPlayed import LastPlayedManger
except ImportError:
    from utils import getCookiesFile
    from CookiesExtraction import interactiveMode as extractCookiesFromBrowser
    from Formatter import SpotifyFormatter
    from LastPlayed import LastPlayedManger


class Spotify:
    """
    Wrapper that makes SpotAPI behave like Spotipy.
    Only implements commonly used methods but can be expanded.
    """

    def __init__(self, login=False, getIsrc=False, cookiesFile=None, email=None, cookies=None, *args, **kwargs):
        self.user_auth = False
        self._next = None
        self.lastPlayedManager = None
        self.recentlyPlayed = deque(maxlen=50)  # type: ignore
        if cookiesFile != None:
            self.login(cookiesFile)
        
        elif email != None and cookies != None: #< allow direct login with cookies for interactive use
            tempFile = getCookiesFile("temp_cookies.json")
            with open(tempFile, "w") as f:
                json.dump(cookies, f)
            self.login(tempFile)

        elif login == True:
            self.login()

        self.getIsrc = False
        if getIsrc:
            try:
                import aiohttp

                self.getIsrc = True
            except:
                print(
                    "aiohttp and asyncio are required for fetching ISRCs. Please install them to use this feature."
                )

    def _getIsrc(self, songId, session=None):
        url = "https://groover.co/core/distantapi/spotify/getdata/"

        headers = {
            "accept": "application/json",
            "origin": "https://groover.co",
            "referer": "https://groover.co/en/lp/free-tools/isrc-finder/",
            "content-type": "application/json",
        }

        payload = {"url": f"https://open.spotify.com/track/{songId}"}

        try:
            if session:  #< if using async
                return session.post(url, headers=headers, json=payload)
            else:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    return ""
                return response.json()["external_ids"]["isrc"]
        except Exception as e:
            print("Could not fetch ISRC:", e)
            return ""

    async def _getIsrc_async(self, session, songId):
        try:
            async with self._getIsrc(songId, session) as resp:
                if resp.status != 200:
                    return songId, ""

                data = await resp.json()
                return songId, data.get("external_ids", {}).get("isrc", "")
        except Exception as e:
            print("Could not fetch ISRC:", e)
            return songId, ""

    def update_recently_played(self, track_uri, played_at, context_uri):
        if not hasattr(self, "recently_played"):
            self.recently_played = SpotifyFormatter.initialRecentlyPlayed(20)

        track_id = track_uri.split(":")[-1]
        track = self.track(track_id)
        entry = SpotifyFormatter.formatRecentlyPlayedItem(track, played_at, context_uri)

        self.recently_played["items"].insert(0, entry)
        if len(self.recently_played["items"]) > 20:
            self.recently_played["items"].pop()

        with open("recently_played_updated.json", "w", encoding="utf-8") as f:
            json.dump(self.recently_played, f, indent=4, ensure_ascii=False)

        return self.recently_played

    def _loginIfNeeded(self):
        if self.isLoggedIn():
            return
        self.login()

    def _addToRecentlyPlayed(self, trackUri, playedAt, contextUri):
        track = self.track(trackUri.split(":")[-1])
        contextId = contextUri.split(":")[-1]
        contextType = contextUri.split(":")[1]
        context = {
            "type": contextType,
            "href": f"https://api.spotify.com/v1/{contextType}s/{contextId}",
            "external_urls": {
                "spotify": f"https://open.spotify.com/{contextType}/{contextId}"
            },
            "uri": contextUri,
        }
        self.recentlyPlayed.append(
            {"track": track, "played_at": playedAt, "context": context}
        )

    def startLastPlayedListener(self):
        self._loginIfNeeded()
        if not self.lastPlayedManager:
            self.lastPlayedManager = LastPlayedManger(self.user_auth)
        self.lastPlayedManager.start(self._addToRecentlyPlayed)

    def next(self, *args, **kwargs):
        return self._next(*args, **kwargs)

    def login(self, cookiesFile=None) -> bool:
        if cookiesFile == None:
            cookiesFile = getCookiesFile()
        try:
            cfg = spotapi.Config(logger=spotapi.Logger())
            saver = spotapi.saver.JSONSaver(cookiesFile)
            try:
                with open(cookiesFile, "r") as f:
                    sessions = json.load(f)
                identifier = sessions[0]["identifier"]
            except:
                raise (f"[-] Could not read sessions file")

            self.user_auth = spotapi.Login.from_saver(saver, cfg, identifier)
        except:
            extractCookiesFromBrowser(cookiesFile)
            return self.login(cookiesFile)
        return True

    def isLoggedIn(self):
        return type(self.user_auth) != bool

    def urlToId(self, url):
        return url.split("/")[-1].split("?")[0]

    def isUrl(self, test):
        return (
            test.startswith("spotify:")
            or test.startswith("https://open.spotify.com/")
            or test.startswith("http://open.spotify.com/")
            or test.startswith("open.spotify")
        )

    def album(self, albumId, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)

        album = spotapi.PublicAlbum(albumId).get_album_info()["data"]["albumUnion"]
        artists = SpotifyFormatter.formatArtists(album["artists"]["items"])
        tracks = SpotifyFormatter.formatTracks(album["tracksV2"]["items"])
        return SpotifyFormatter.formatAlbum(album, artists, tracks)

    def album_tracks(self, albumId, limit=-1, offset=0, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)

        allTracks = []
        for tracks in spotapi.PublicAlbum(albumId).paginate_album():
            allTracks.extend(tracks)
        allTracks = SpotifyFormatter.formatTracks(allTracks)

        total = len(allTracks)
        if limit == -1:
            limit = total
        end = offset + limit
        # items = allTracks[offset:end]
        return SpotifyFormatter.addChunkInfo(allTracks, total, limit, offset, end)
        # return({"items": allTracks, "next": False})

    def artist(self, artistId, *args, **kwargs):
        if self.isUrl(artistId):
            artistId = self.urlToId(artistId)

        try:
            artist = spotapi.Artist().get_artist(artistId)["data"]["artistUnion"]
            artist["name"] = artist["profile"]["name"]
            artist["genres"] = [""]
        except:
            artist = {
                "name": "Not Found",
                "id": artistId,
                "uri": f"spotify:artist:{artistId}",
                "external_urls": {
                    "spotify": f"https://open.spotify.com/artist/{artistId}"
                },
                "genres": [""],
            }
        return artist

    def artist_albums(
        self, artistId, limit=-1, offset=0, include_groups="album", *args, **kwargs
    ):
        allowed = set(include_groups.split(","))
        discog = spotapi.Artist().get_artist(artistId)["data"]["artistUnion"][
            "discography"
        ]

        merged = []
        for group_name, group_data in discog.items():
            if group_name in allowed:
                if isinstance(group_data, dict) and "items" in group_data:
                    merged.extend(group_data["items"])

        total = len(merged)
        if limit == -1:
            limit = total
        end = offset + limit
        # items = merged[offset:end]
        return SpotifyFormatter.addChunkInfo(merged, total, limit, offset, end)

    def playlist(self, playlistId, limit=-1, offset=0, *args, **kwargs):
        playlist = spotapi.PublicPlaylist(playlistId).get_playlist_info()["data"][
            "playlistV2"
        ]
        return SpotifyFormatter.formatPlaylist(playlist)

    async def playlist_items_async(
        self, playlistId, limit=50, offset=0, *args, **kwargs
    ):
        if self.isUrl(playlistId):
            playlistId = self.urlToId(playlistId)

        allTracks = []
        tasks = []
        session = None

        if self.getIsrc:
            session = aiohttp.ClientSession()  # type: ignore

        try:
            for chunk in spotapi.PublicPlaylist(playlistId).paginate_playlist():
                for track in chunk["items"]:
                    try:
                        meta = SpotifyFormatter.formatPlaylistTrack(track)
                        allTracks.append(meta)

                        if self.getIsrc:
                            tasks.append(
                                self._getIsrc_async(session, meta["track"]["id"])
                            )
                    except:
                        pass

            if self.getIsrc and tasks:
                results = await asyncio.gather(*tasks)  # type: ignore
                isrc_map = dict(results)

                for meta in allTracks:
                    sid = meta["track"]["id"]
                    meta["track"]["external_ids"]["isrc"] = isrc_map.get(sid, "")

        finally:
            if session:
                await session.close()

        total = len(allTracks)
        if limit == -1:
            limit = total

        end = offset + limit
        return SpotifyFormatter.addChunkInfo(allTracks, total, limit, offset, end)

    def playlist_items(self, *args, **kwargs):
        try:
            loop = (
                asyncio.get_event_loop()
            )  #< bind to async thread if already exists # type: ignore
            return loop.run_until_complete(self.playlist_items_async(*args, **kwargs))
        except RuntimeError:
            return asyncio.run(self.playlist_items_async(*args, **kwargs))  # type: ignore

    def track(self, trackId, *args, **kwargs):
        if self.isUrl(trackId):
            trackId = self.urlToId(trackId)

        track = spotapi.Song().get_track_info(trackId)["data"]["trackUnion"]
        try:
            artists = track["firstArtist"]["items"]
            artists.extend(track["otherArtists"]["items"])
        except:
            artists = ["Not Found"]
        formattedArtists = SpotifyFormatter.formatArtists(artists)
        track = SpotifyFormatter.formatTrack(track, formattedArtists)
        if self.getIsrc:
            track["external_ids"] = {"isrc": self._getIsrc(track["track_id"])}
        return track

    def search(self, query, limit=50, offset=0, type="track", *args, **kwargs):
        pages = spotapi.Public().song_search(query)
        for results in pages:  #< save first page
            break

        tracks = []
        for res in results:
            res = res["item"]["data"]
            if res["__typename"] != "Track":  #< only accept tracks
                continue
            formattedArtists = SpotifyFormatter.formatArtists(res["artists"]["items"])
            meta = SpotifyFormatter.formatTrack(res, formattedArtists)
            if self.getIsrc:
                meta["external_ids"] = {"isrc": self._getIsrc(meta["track_id"])}
            tracks.append(meta)

        total = len(tracks)

        if limit == -1:
            limit = total

        end = offset + limit
        return {
            "tracks": SpotifyFormatter.addChunkInfo(tracks, total, limit, offset, end)
        }

    def current_user_saved_tracks(self, limit=-1, offset=0, *args, **kwargs):
        self._loginIfNeeded()

        pl = spotapi.playlist.PrivatePlaylist(self.user_auth).paginate_saved_tracks()
        tracks = []
        for raws in pl:
            for raw in raws["items"]:
                addedAt = raw["addedAt"]["isoString"]
                songId = raw["track"]["_uri"].removeprefix("spotify:track:")
                track = raw["track"]["data"]
                try:
                    artists = track["artists"]["items"]
                except:
                    artists = ["Not Found"]
                artists = SpotifyFormatter.formatArtists(artists)
                meta = SpotifyFormatter.formatTrack(track, artists, songId=songId)
                if self.getIsrc:
                    meta["external_ids"] = {"isrc": self._getIsrc(meta["track_id"])}
                tracks.append({"added_at": addedAt, "track": meta})

        total = len(tracks)
        if limit == -1:
            limit = total
        end = offset + limit
        result = SpotifyFormatter.addChunkInfo(tracks, total, limit, offset, end)
        result["href"] = (
            f"https://api.spotify.com/v1/me/tracks?offset={offset}&limit={limit}"
        )
        return result

    def current_user_recently_played(self, limit=50, after=None, before=None):
        self._loginIfNeeded()
        return spotapi.player.PlayerStatus(self.user_auth).last_songs_played

    def user_playlists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.user_playlists(limit=limit, offset=offset + limit)
        return

    def current_user_playlists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.current_user_playlists(
            limit=limit, offset=offset + limit
        )
        return

    def current_user_playlists(self, limit=50, offset=0):
        """Get current user playlists without required getting his profile
        Parameters:
            - limit  - the number of items to return
            - offset - the index of the first item to return
        """
        pass

    def current_user_followed_artists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.current_user_followed_artists(
            limit=limit, offset=offset + limit
        )
        return

    def me(self):
        """Get detailed profile information about the current user.
        An alias for the 'current_user' method.
        """
        pass


if __name__ == "__main__":
    import json

    try:
        import pysole  # type: ignore
    except:
        pysole = None
        print("To get an interactive console, do pip install liveConsole")

    def save(jsonData, name="saved.json"):
        with open(name, "w") as f:
            json.dump(jsonData, f, indent=4)

    sp = Spotify()
    sp.login()
    # a = spotapi.player.Player(sp.user_auth)
    status = spotapi.player.PlayerStatus(sp.user_auth)
    sp.startLastPlayedListener()
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=True)
    playlist = sp.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
    save(playlist, "playlist.json")
    track = sp.track("67Hna13dNDkZvBpTXRIaOJ")
    save(track, "track.json")
    album = sp.album("4m2880jivSbbyEGAKfITCa")
    save(album, "album.json")
    albumTracks = sp.album_tracks("4m2880jivSbbyEGAKfITCa")
    save(albumTracks, "album_tracks.json")
    saved = sp.current_user_saved_tracks()
    save(saved, "saved_tracks.json")
    self = sp
