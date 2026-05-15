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

    def updateLoop(self, callback):
        while self.run:
            try:
                timestamp = int(self.manager.state.timestamp) / 1000
                if self.lastPLayed != self.manager.state.track.uid:
                    currentTrackUri = self.manager.state.track.uri
                    playedAt = (
                        datetime.datetime.fromtimestamp(
                            timestamp, tz=datetime.timezone.utc
                        )
                        .isoformat()
                        .replace("+00:00", "Z")
                    )
                    callback(currentTrackUri, playedAt, self.manager.state.context_uri)
                    self.lastPLayed = self.manager.state.track.uid
                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)

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
