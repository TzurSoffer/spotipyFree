import spotapi
class Spotify:
    """
    Wrapper that makes SpotAPI behave like Spotipy.
    Only implements commonly used methods but can be expanded.
    """

    def __init__(self, username=None, password=None):
        self.user_auth = False
        self._next = None
        if username != None:
            self.user_auth = True
            raise Exception("Login not yet implemented")
    
    def urlToId(self, url):
        return(url.split("/")[-1].split("?")[0])
    
    def isUrl(self, test):
        return(test.startswith("spotify:") or test.startswith("https://open.spotify.com/") or test.startswith("open.spotify"))
    
    def _getArtists(self, artists):
        for artist in artists:
            artist["name"] = artist["profile"]["name"]
            artist["external_urls"] = {"spotify": artist["uri"]}
            artist.pop("profile", None)
            artist.pop("discography", None)
            artist.pop("visuals", None)
            artist.pop("relatedContent", None)
        return(artists)
    
    def _getTracksFromPlaylist(self, paginate):
        allTracks = []
        for chunk in paginate:
            for track in chunk["items"]:
                track = track["itemV3"]["data"]
                meta = {"track": {
                    "name": track['identityTrait']["name"],
                    "id": track["uri"].removeprefix("spotify:track:"),
                    "duration_ms": track["consumptionExperienceTrait"]["duration"]["seconds"]/1000+track["consumptionExperienceTrait"]["duration"]["nanoSeconds"]*1_000_000,
                    "description": track["identityTrait"]["description"],
                    "artists": track["identityTrait"]["contributors"]["items"],
                    "album": {},
                    "type": track["identityTrait"]["type"],
                    "external_urls": {"spotify": track["identityTrait"]["contentHierarchyParent"]["uri"]},
                    "is_local": False,
                    "disc_number": 0,     #< idk
                    "track_number": 0,    #< idk
                    "explicit": False,    #< idk
                    "external_ids": {},   #< idk
                    
                }}
                allTracks.append(meta)
        
        return(allTracks)

    def _formatAlbum(self, items, total, limit, offset, end):
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "next": end if end < total else None,
            "previous": offset - limit if offset - limit >= 0 else None
        }

    def _formatTracks(self, tracks):
        allTracks = []
        for track in tracks:
            uid = track["uid"]
            track = track["track"]
            meta = {
                "name": track["name"],
                "external_urls": {"spotify": uid},
                "duration_ms": ["duration"],
                "disc_number": track["discNumber"],
                "track_number": track["trackNumber"],
                "artists": self._getArtists(track["artists"]["items"]),
                "explicit": track["contentRating"]["label"] == "EXPLICIT",

            }
            allTracks.append(meta)
        
        return(allTracks)

    def next(self, *args, **kwargs):
        return(self._next(*args, **kwargs))

    def album(self, albumId, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)

        album = spotapi.PublicAlbum(albumId).get_album_info()["data"]["albumUnion"]
        artists = self._getArtists(album["artists"]["items"])
        album["artists"] = artists
        album["tracks"] = self._formatTracks(album["tracksV2"]["items"])
        album["total_tracks"] = len(album["tracks"]),
        album["images"] = album["coverArt"]["sources"],
        album["album_type"] = "",

        return(album)

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
        return(self._formatAlbum(allTracks, total, limit, offset, end))
        # return({"items": allTracks, "next": False})
    
    def artist(self, artistId, *args, **kwargs):
        if self.isUrl(artistId):
            artistId = self.urlToId(artistId)
        return(spotapi.Artist().get_artist(artistId))
    
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
        return(self._formatAlbum(merged, total, limit, offset, end))
    
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
    
    def playlist_items(self, playlistId, limit=50, offset=0, *args, **kwargs):
        if self.isUrl(playlistId):
            playlistId = self.urlToId(playlistId)
            
        allTracks = self._getTracksFromPlaylist(spotapi.PublicPlaylist(playlistId).paginate_playlist())

        total = len(allTracks)

        if limit == -1:
            limit = total

        end = offset + limit
        # items = allTracks[offset:end]
        return(self._formatAlbum(allTracks, total, limit, offset, end))

    def track(self, trackId, *args, **kwargs):
        if self.isUrl(trackId):
            trackId = self.urlToId(trackId)
        
        track = spotapi.Song().get_track_info(trackId)["data"]["trackUnion"]
        artists = track["firstArtist"]["items"]
        artists.extend(track["otherArtists"]["items"])
        artists = self._getArtists(artists)
        meta = {
            "name": track["name"],
            "id": track["id"],
            "disc_number": track["trackNumber"],
            "track_number": track["trackNumber"],
            "duration_ms": track["duration"]["totalMilliseconds"],
            "artists": artists,
            "album": track["albumOfTrack"],
            "explicit": track["contentRating"]["label"] == "EXPLICIT",
            "external_ids": {}
            
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
        return(self._formatAlbum(sliced, total, limit, offset, end))

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
    import pysole
    pysole.probe(runRemainingCode=True, printStartupCode=True)
    playlist = sp.playlist_items("6lnfkAgnVtNzvj8KScLSkj")
    track = sp.track("67Hna13dNDkZvBpTXRIaOJ")
    album = sp.album("4m2880jivSbbyEGAKfITCa")
    albumTracks = sp.album_tracks("4m2880jivSbbyEGAKfITCa")