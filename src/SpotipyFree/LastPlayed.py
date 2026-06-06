import time
from spotapi.status import PlayerStatus
import datetime
import threading


class LastPlayedManger:
    def __init__(self, login):
        self.thread = None
        self.run = False
        self.login = login
        self.manager = PlayerStatus(login)
        self.lastPLayed = ""
        self.lastTrackUri = None
        self.lastPlayedAt = None
        self.lastContextUri = None

    def updateLoop(self, callback):
        while self.run:
            try:
                timestamp = int(self.manager.state.timestamp) / 1000
                if self.lastPLayed != self.manager.state.track.uid:
                    if self.lastTrackUri != None:
                        timePlayed = max(0, int((time.time() - self.lastPlayedAt.timestamp()) * 1000))
                        callback(self.lastTrackUri, self.lastPlayedAtText, self.lastContextUri, timePlayed)
                    self.lastTrackUri = self.manager.state.track.uri
                    self.lastPlayedAt = (
                        datetime.datetime.fromtimestamp(
                            timestamp, tz=datetime.timezone.utc
                        )
                    )
                    self.lastPlayedAtText = self.lastPlayedAt.isoformat().replace("+00:00", "Z")
                    self.lastContextUri = self.manager.state.context_uri
                    self.lastPLayed = self.manager.state.track.uid
                time.sleep(3)
            except Exception as e:
                print(f"[SpotipyFree] Error in Recently Played: {e}")
                time.sleep(10)
                try:
                    self.manager.reconnect()
                except:
                    print(f"[SpotipyFree] Listener stopped due to websocket disconnection. To reconnect, you must use run pip uninstall spotAPI and then pip install git+https://github.com/TzurSoffer/SpotAPI/")

    def start(self, callback):
        self.run = True
        self.thread = threading.Thread(target=self.updateLoop, args=(callback,))
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.run = False
        self.thread.join()


if __name__ == "__main__":

    import SpotipyFree

    sp = SpotipyFree.Spotify()
    sp.login()
