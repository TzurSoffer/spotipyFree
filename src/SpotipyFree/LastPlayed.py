import time
from spotapi.status import PlayerStatus
import datetime
import json

class LastPlayedManger:
    def __init__(self, login):
        self.login = login
        self.manager = PlayerStatus(login)
        self.lastPLayed = None

        recently_played = {
            "items": [],
            "limit": 20,
            "href": "https://api.spotify.com/v1/me/player/recently-played?limit=20",
            "cursors": {"after": None, "before": None},
            "next": None
        }
    
    def updateLoop(self, callbackOnNewSong):
        while True:
            try:
                current_state = self.manager.state
                current_track = current_state.track
                current_track_uri = current_track.uri if current_track else None
                
                if current_track_uri and current_track_uri != previous_track_uri:
                    metadata = current_track.metadata if current_track else {}
                    title = metadata.title if metadata else "Unknown"
                    
                    played_at = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
                    
                    track_dict = {
                        "name": title,
                        "id": current_track_uri.split(":")[-1] if current_track_uri else "",
                        "uri": current_track_uri,
                        "artists": [{"name": "Unknown"}],  # Simplified
                        "album": {"name": metadata.album_title if metadata else "Unknown"},
                        "duration_ms": 0,  # Not available in PlayerState
                        "external_urls": {"spotify": f"https://open.spotify.com/track/{current_track_uri.split(':')[-1]}" if current_track_uri else ""},
                        "explicit": False,
                        "type": "track",
                        "popularity": 0
                    }
                    
                    context = {
                        "type": "unknown",
                        "uri": current_state.context_uri or "",
                        "external_urls": {"spotify": ""},
                        "href": ""
                    }
                    
                    entry = {
                        "track": track_dict,
                        "played_at": played_at,
                        "context": context
                    }
                    
                    self.lastPlayed["items"].insert(0, entry)
                    
                    if len(self.lastPlayed["items"]) > 20:
                        self.lastPlayed["items"].pop()
                    
                    with open("recently_played_updated.json", "w") as f:
                        json.dump(self.lastPlayed, f, indent=4)
                    
                    print(f"New song: {title}")
                    previous_track_uri = current_track_uri
                
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

    
if __name__ == "__main__":

    import SpotipyFree
    sp = SpotipyFree.Spotify()
    sp.login()


