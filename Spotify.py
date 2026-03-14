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
    
    def _formatAlbum(self, items, total, limit, offset, end):
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "next": end if end < total else None,
            "previous": offset - limit if offset - limit >= 0 else None
        }
    
    def next(self, *args, **kwargs):
        return(self._next(*args, **kwargs))
        
    def album(self, albumId, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)
        return(spotapi.PublicAlbum(albumId).get_album_info()["data"]["albumUnion"])

    def album_tracks(self, albumId, limit=-1, offset=0, *args, **kwargs):
        if self.isUrl(albumId):
            albumId = self.urlToId(albumId)

        totalTracks = []
        for chunk in spotapi.PublicAlbum(albumId).paginate_album():
            totalTracks.extend(chunk)

        total = len(totalTracks)
        if limit == -1:
            limit = total
        end = offset + limit
        # items = totalTracks[offset:end]
        return(self._formatAlbum(totalTracks, total, limit, offset, end))
        # return({"items": totalTracks, "next": False})
    
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
        # self._next = lambda: self.playlist(limit=limit, offset=offset+limit)
        return(spotapi.PublicPlaylist(playlistId).get_playlist_info()["data"]["playlistV2"])
    
    def playlist_items(self, playlistId, limit=50, offset=0, *args, **kwargs):
        if self.isUrl(playlistId):
            playlistId = self.urlToId(playlistId)

        allTracks = []
        for chunk in spotapi.PublicPlaylist(playlistId).paginate_playlist():
            allTracks.extend(chunk)

        total = len(allTracks)

        if limit == -1:
            limit = total

        end = offset + limit
        items = allTracks[offset:end]
        return(self._formatAlbum(items, total, limit, offset, end))

    def track(self, trackId, *args, **kwargs):
        if self.isUrl(trackId):
            trackId = self.urlToId(trackId)
        return(spotapi.PublicTrack(trackId).get_track_info()["data"]["trackUnion"])

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
    pysole.probe()