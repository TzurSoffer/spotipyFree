import requests
import spotapi

class Spotify:
    """
    Wrapper that makes SpotAPI behave like Spotipy.
    Only implements commonly used methods but can be expanded.
    """

    def __init__(self, username=None, password=None, getIsrc=False, *args, **kwargs):
        self.user_auth = False
        self.use_cache_file = False
        self.no_cache = True
        self._next = None
        if username != None:
            self.user_auth = True
            raise Exception("Login not yet implemented")
        self.getIsrc = False
        if getIsrc:
            try:
                import aiohttp
                import asyncio
                self.getIsrc = True
            except:
                print("aiohttp and asyncio are required for fetching ISRCs. Please install them to use this feature.")
                self.getIsrc = False

    @staticmethod
    def init(*args, **kwargs):
        return
    
    def urlToId(self, url):
        return(url.split("/")[-1].split("?")[0])
    
    def isUrl(self, test):
        return(test.startswith("spotify:") or test.startswith("https://open.spotify.com/") or test.startswith("open.spotify"))

    def _getIsrc(self, songId, session=None):
        url = "https://groover.co/core/distantapi/spotify/getdata/"

        headers = {
            "accept": "application/json",
            "origin": "https://groover.co",
            "referer": "https://groover.co/en/lp/free-tools/isrc-finder/",
            "content-type": "application/json",
        }

        payload = {
            "url": f"https://open.spotify.com/track/{songId}"
        }

        try:
            if session:  #< if using async
                return session.post(url, headers=headers, json=payload)
            else:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    return("")
                return(response.json()["external_ids"]["isrc"])
        except Exception as e:
            print("Could not fetch ISRC:", e)
            return("")

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

    def _getArtists(self, artists):
        for i, artist in enumerate(artists):
            if type(artist) == str:
                artists[i] = {
                    "Name": "",
                    "href": "",
                    "external_urls": {"spotify": ""},
                    "genres": [""]
                }
                continue
            artist["name"] = artist["profile"]["name"]
            artist["external_urls"] = {"spotify": artist["uri"].replace("spotify:artist:", "https://open.spotify.com/artist/")}
            artist["href"] = artist["uri"].replace("spotify:artist:", "https://api.spotify.com/v1/artists/")
            artist["genres"] = [""]
            artist.pop("profile", None)
            artist.pop("discography", None)
            artist.pop("visuals", None)
            artist.pop("relatedContent", None)
        return(artists)

    def _addChunkInfo(self, items, total, limit, offset, end):
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "next": False,
            "previous": offset - limit if offset - limit >= 0 else None
        }

    def _formatTracks(self, tracks):
        allTracks = []
        for track in tracks:
            track = track["track"]
            trackId = track["uri"].removeprefix("spotify:track:")
            url = "https://open.spotify.com/track/"+trackId
            meta = {
                "name": track["name"],
                "id": trackId,
                "song_id": trackId,
                "url": url,
                "external_urls": {"spotify": url},
                "duration_ms": track["duration"]["totalMilliseconds"],
                "disc_number": track["discNumber"],
                "track_number": track["trackNumber"],
                "artists": self._getArtists(track["artists"]["items"]),
                "explicit": track["contentRating"]["label"] == "EXPLICIT",

            }
            allTracks.append(meta)
        
        return(allTracks)

    def next(self, *args, **kwargs):
        return(self._next(*args, **kwargs))

    def _formatAlbum(self, album, artists, tracks):
        album["id"] = album["uri"].removeprefix("spotify:album:")
        album["artists"] = artists
        album["tracks"] = {"items": tracks}
        album["total_tracks"] = len(album["tracks"]["items"])
        album["images"] = album["coverArt"]["sources"]
        album["release_date"] = album["date"]["isoString"].split("T")[0]
        album["album_type"] = "album"
        album["copyrights"] = [{"text": "", "type": ""}]
        album["genres"] = [""]
        return(album)

    def album(self, albumId, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)

        album = spotapi.PublicAlbum(albumId).get_album_info()["data"]["albumUnion"]
        artists = self._getArtists(album["artists"]["items"])
        tracks = self._formatTracks(album["tracksV2"]["items"])
        return(self._formatAlbum(album, artists, tracks))

    def album_tracks(self, albumId, limit=-1, offset=0, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)
        
        allTracks = []
        for tracks in spotapi.PublicAlbum(albumId).paginate_album():
            allTracks.extend(tracks)
        allTracks = self._formatTracks(allTracks)

        total = len(allTracks)
        if limit == -1:
            limit = total
        end = offset + limit
        # items = allTracks[offset:end]
        return(self._addChunkInfo(allTracks, total, limit, offset, end))
        # return({"items": allTracks, "next": False})
    
    def artist(self, artistId, *args, **kwargs):
        if self.isUrl(artistId):
            artistId = self.urlToId(artistId)
            
        artist = spotapi.Artist().get_artist(artistId)["data"]["artistUnion"]
        artist["name"] = artist["profile"]["name"]
        artist["genres"] = [""]
        return(artist)
    
    def artist_albums(self, artistId, limit=-1, offset=0, include_groups="album", *args, **kwargs):
        allowed = set(include_groups.split(","))
        discog = spotapi.Artist().get_artist(artistId)["data"]["artistUnion"]["discography"]

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
        return(self._addChunkInfo(merged, total, limit, offset, end))
    
    def playlist(self, playlistId, limit=-1, offset=0, *args, **kwargs):
        playlist = spotapi.PublicPlaylist(playlistId).get_playlist_info()["data"]["playlistV2"]
        playlist["owner"] = playlist["ownerV2"]["data"]
        playlist.pop("ownerV2", None)
        playlist["owner"]["display_name"] = playlist["owner"]["name"]
        playlist["external_urls"] = {}
        playlist["external_urls"]["spotify"] = playlist["owner"]["uri"]
        try:
            playlist["images"] = playlist["images"]["items"][-1]["sources"]
        except:
            playlist["images"] = []
        
        return(playlist)
    
    async def playlist_items_async(self, playlistId, limit=50, offset=0, *args, **kwargs):
        if self.isUrl(playlistId):
            playlistId = self.urlToId(playlistId)

        allTracks = []
        tasks = []
        session = None

        if self.getIsrc:
            session = aiohttp.ClientSession() # type: ignore

        try:
            for chunk in spotapi.PublicPlaylist(playlistId).paginate_playlist():
                for track in chunk["items"]:
                    try:
                        trackV3 = track["itemV3"]["data"]
                        trackV2 = track["itemV2"]["data"]

                        trackType = "track" if trackV2["mediaType"] == "AUDIO" else "None"
                        songId = trackV3["uri"].removeprefix("spotify:track:")

                        meta = {"track": {
                            "name": trackV3['identityTrait']["name"],
                            "id": songId,
                            "duration_ms": trackV2["trackDuration"]["totalMilliseconds"],
                            "description": trackV3["identityTrait"]["description"],
                            "artists": trackV3["identityTrait"]["contributors"]["items"],
                            "album": {},
                            "type": trackType,
                            "external_urls": {
                                "spotify": "https://open.spotify.com/track/" +
                                trackV2["uri"].removeprefix("spotify:track:")
                            },
                            "is_local": False,
                            "disc_number": trackV2["discNumber"],
                            "track_number": trackV2["trackNumber"],
                            "explicit": trackV2["contentRating"]["label"] == "EXPLICIT",
                            "external_ids": {"isrc": ""}
                        }}

                        allTracks.append(meta)

                        if self.getIsrc:
                            tasks.append(self._getIsrc_async(session, songId))

                    except:
                        pass

            if self.getIsrc and tasks:
                results = await asyncio.gather(*tasks) # type: ignore
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
        return self._addChunkInfo(allTracks, total, limit, offset, end)

    def playlist_items(self, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()   #< bind to async thread if already exists # type: ignore
            return(loop.run_until_complete(
                self.playlist_items_async(*args, **kwargs)
            ))
        except RuntimeError:
            return(asyncio.run(self.playlist_items_async(*args, **kwargs))) # type: ignore

    def track(self, trackId, *args, **kwargs):
        if self.isUrl(trackId):
            trackId = self.urlToId(trackId)
        
        track = spotapi.Song().get_track_info(trackId)["data"]["trackUnion"]
        try:
            artists = track["firstArtist"]["items"]
            artists.extend(track["otherArtists"]["items"])
        except:
            artists = ["Not Found"]
        artists = self._getArtists(artists)
        songId = track["uri"].removeprefix("spotify:track:")
        meta = {
            "name": track["name"],
            "id": track["id"],
            "disc_number": track["trackNumber"],
            "track_number": track["trackNumber"],
            "duration_ms": track["duration"]["totalMilliseconds"],
            "artists": artists,
            "album": self._formatAlbum(track["albumOfTrack"], artists, tracks=track["albumOfTrack"]["tracks"]["items"]),
            "explicit": track["contentRating"]["label"] == "EXPLICIT",
            "external_urls": {"spotify": "https://open.spotify.com/track/"+track["uri"].removeprefix("spotify:track:")},
            "popularity": 10, #< needs fixing
            "type": "track",
            "external_ids": {
                "isrc": self._getIsrc(songId) if self.getIsrc else ""
            }
        }
        
        return(meta)

    def search(self, query, limit=50, offset=0, type="track", *args, **kwargs):
        results = spotapi.Search().search(query)["data"]

        key = type + "s"
        items = results.get(key, {}).get("items", [])

        total = len(items)

        if limit == -1:
            limit = total

        end = offset + limit
        sliced = items[offset:end]

        self._next = lambda: self.search(query, limit=limit, offset=end, type=type)
        return(self._addChunkInfo(sliced, total, limit, offset, end))

    def current_user_saved_tracks(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.current_user_saved_tracks(limit=limit, offset=offset+limit)
        return
    
    def user_playlists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.user_playlists(limit=limit, offset=offset+limit)
        return
    
    def current_user_playlists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.current_user_playlists(limit=limit, offset=offset+limit)
        return
    
    def current_user_followed_artists(self, limit=-1, offset=0, *args, **kwargs):
        self._next = lambda: self.current_user_followed_artists(limit=limit, offset=offset+limit)
        return

if __name__ == "__main__":
    sp = Spotify()
    try:
        import pysole  # type: ignore
    except:
        pysole = None
        print("To get an interactive console, do pip install liveConsole")
    if pysole:
        pysole.probe(runRemainingCode=True, printStartupCode=True)
    playlist = sp.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
    track = sp.track("67Hna13dNDkZvBpTXRIaOJ")
    album = sp.album("4m2880jivSbbyEGAKfITCa")
    albumTracks = sp.album_tracks("4m2880jivSbbyEGAKfITCa")