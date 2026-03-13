import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SpotifyTemplate:
    def current_playback(self, SongID="", songName="", PlaylistId="", ArtistId="", artistsName="", AlbumID=""):
        return({'device': {
            'id': '',
            'is_active': False,
            'is_private_session': False,
            'is_restricted': False,
            'name': 'TZUR-COMPUTER',
            'supports_volume': False,
            'type': 'Computer',
            'volume_percent': 100},
            'shuffle_state': False,
            'smart_shuffle': False,
            'repeat_state': 'off',
            'is_playing': False,
            'timestamp': 0,
            'context': {
                'external_urls': {
                    'spotify': f'https://open.spotify.com/playlist/{PlaylistId}'},
                    'href': f'https://api.spotify.com/v1/playlists/{PlaylistId}',
                    'type': 'playlist',
                    'uri': f'spotify:playlist:{PlaylistId}'
                    },
                    'progress_ms': 154329,
                    'item': {
                        'album': {
                            'album_type': 'compilation',
                            'artists': [
                                {'external_urls': {
                                    'spotify': f'https://open.spotify.com/artist/{ArtistId}'},
                                    'href': f'https://api.spotify.com/v1/artists/{ArtistId}',
                                    'id': ArtistId,
                                    'name': artistsName,
                                    'type': 'artist',
                                    'uri': f'spotify:artist:{ArtistId}'
                                    }
                                    ],
                                    'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'],
                                    'external_urls': {
                                        'spotify': f'https://open.spotify.com/album/{AlbumID}'},
                                        'href': f'https://api.spotify.com/v1/albums/{AlbumID}',
                                        'id': AlbumID,
                                        'images': [
                                            {'height': 640,
                                            'url': 'https://i.scdn.co/image/ab67616d0000b273383811a9b3081023c612fb7b',
                                            'width': 640},
                                            {'height': 300,
                                            'url': 'https://i.scdn.co/image/ab67616d00001e02383811a9b3081023c612fb7b',
                                            'width': 300},
                                            {'height': 64,
                                            'url': 'https://i.scdn.co/image/ab67616d00004851383811a9b3081023c612fb7b',
                                            'width': 64}],
                                            'name': 'The Anthology',
                                            'release_date': '1998-06-16',
                                            'release_date_precision': 'day',
                                            'total_tracks': 48,
                                            'type': 'album',
                                            'uri': f'spotify:album:{AlbumID}'},
                                            'artists': [
                                                {
                                                    'external_urls': {
                                                        'spotify': 'https://open.spotify.com/artist/ArtistId'},
                                                        'href': 'https://api.spotify.com/v1/artists/ArtistId',
                                                        'id': ArtistId,
                                                        'name': artistsName,
                                                        'type': 'artist',
                                                        'uri': f'spotify:artist:{ArtistId}'}],
                                                        'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'],
                                                        'disc_number': 2,
                                                        'duration_ms': 162733,
                                                        'explicit': False,
                                                        'external_ids': {'isrc': 'USMC15472746'},
                                                        'external_urls': {
                                                            'spotify': f'https://open.spotify.com/track/{SongID}'},
                                                            'href': f'https://api.spotify.com/v1/tracks/{SongID}',
                                                            'id': SongID,
                                                            'is_local': False,
                                                            'name': songName,
                                                            'popularity': 48,
                                                            'preview_url': None,
                                                            'track_number': 11,
                                                            'type': 'track',
                                                            'uri': f'spotify:track:{SongID}'},
                                                            'currently_playing_type': 'track',
                                                            'actions': {'disallows': {'resuming': True}}
        })

class Spotify(SpotifyTemplate):
    def __init__(self, username, password, stealth=True, *args, **kwargs):
        self.username = username
        self.password = password
        self._cookieFile = f"spotify_cookies_{self.username}.json"

        opts = Options()
        if stealth:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
            opts.add_argument("--force-device-scale-factor=1")
            opts.add_argument("--high-dpi-support=1")
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_argument("--enable-gpu")
            opts.add_argument("--disable-software-rasterizer")
            opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")


        self.driver = webdriver.Chrome(options=opts)

        # Attempt to restore an existing session using stored cookies
        self.driver.get("https://open.spotify.com")
        self._loadCookies()
        if  self._isLoggedIn():
            print("Restored session from saved cookies.")
        else:
            print("Invalid cookies, logging in.")
            if self._login():
                print("Saving new cookies")
                self._saveCookies()

        self._removeUnneededWindow()
    
    def _clickButtonByText(self, text):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(., '{text}')]")
            )
        ).click()
    
    def _findClickableByMod(self, modifier, value, type="", timeout=5):
        return(WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"{type}[{modifier}='{value}']")
            )
        ))

    def _getPlaylists(self) -> dict:
        rows = self.driver.find_elements(
            By.CSS_SELECTOR,
            'div[data-encore-id="listRow"][role="group"]'
        )

        playlists = {}

        for row in rows:
            try:
                titleElement= row.find_element(By.CSS_SELECTOR, '[data-encore-id="listRowTitle"]')
                name = titleElement.text.strip()

                aria = row.get_attribute("aria-labelledby")
                if "spotify:playlist:" not in aria:
                    continue
                playlistId = aria.split("spotify:playlist:")[-1]

                url = f"https://open.spotify.com/playlist/{playlistId}"

                playlists[name] = url
            except:
                continue

        return(playlists)
    
    def _login(self) -> bool:
        try:
            self.driver.get("https://accounts.spotify.com/en/login")

            box = self._findClickableByMod("data-testid", "login-username", "input")

            box.clear()
            box.send_keys(self.username)
            box.send_keys(Keys.ENTER)

            # find log in with password button
            try:
                self._clickButtonByText("Log in with a password")
                print("Button found and clicked.")
            except:
                print("Button not found.")

            # put in password
            box = self._findClickableByMod("data-testid", "login-password", "input")

            box.clear()
            box.send_keys(self.password)
            box.send_keys(Keys.ENTER)

            self._findClickableByMod("data-testid", "web-player-link", "button").click()
            return(True)
        except:
            return(False)

    def _cookiesPath(self) -> Path:
        return(Path(__file__).resolve().parent / self._cookieFile)

    def _loadCookies(self) -> bool:
        path = self._cookiesPath()
        if not path.exists():
            return(False)

        try:
            with open(path, "r", encoding="utf-8") as f:
                cookies = json.load(f)

            for cookie in cookies:
                cookie = {k: v for k, v in cookie.items() if k not in ("sameSite",)}
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    continue

            self.driver.refresh()
            return(True)
        except Exception:
            return(False)

    def _saveCookies(self) -> bool:
        try:
            cookies = self.driver.get_cookies()
            path = self._cookiesPath()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            return(True)
        except Exception:
            return(False)

    def _isLoggedIn(self) -> bool:
        try:
            url = self.driver.current_url
            if "accounts.spotify.com" in url and "_authfailed=1" in url:
                return(False)
            self._findClickableByMod("data-testid", "login-button", "button", timeout=2)
            return(False)
        except:
            return(True)

    def _removeUnneededWindow(self) -> bool:
        """ remove main page (contains links to playlists that we dont want to find) """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "main-view-container"))
            )
            self.driver.execute_script("""
            const el = document.querySelector('.main-view-container');
            if (el) el.style.display = 'none';
            """)
            self.driver.execute_script("""
            const el = document.querySelector('.a_fKt7xvd8od_kEb');
            if (el) el.style.display = 'none';
            """)
            return(True)
        except:
            return(False)

    def getCurrentTrackData(self):
        self.driver.get("https://open.spotify.com/queue")
        
        songName = self._findClickableByMod("data-testid", "context-item-link", "a").text
        artistName = self._findClickableByMod("data-testid", "context-item-info-subtitles", "div").text.split(", ")
        
        # Wait for the Now Playing row
        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'ul[aria-label="Now playing"] li')
            )
        )

        # Open the ... menu
        menu_button = row.find_element(
            By.CSS_SELECTOR,
            'button[data-testid="more-button"]'
        )
        menu_button.click()
        time.sleep(0.2)

        menu = self.driver.find_element(By.ID, "context-menu")

        # Album link
        albumLink = menu.find_element(By.XPATH, ".//a[contains(@href, '/album/')]").get_attribute("href")

        # Extract track ID from highlight param
        # Example: ?highlight=spotify:track:6AtupSalvtkvfUjJLMl2Q3
        trackId = None
        albumId = None
        if "highlight=spotify:track:" in albumLink:
            albumLink, trackId = albumLink.split("highlight=spotify:track:")
            albumId = albumLink.replace("/album/", "")

        trackUrl = f"https://open.spotify.com/track/{trackId}" if trackId else None

        # Artist link
        artistLink = menu.find_element(By.XPATH, ".//a[contains(@href, '/artist/')]").get_attribute("href")
        artistId = artistLink.split("artist/")
        if len(artistId) > 1:
            artistId = artistId[1]
        else:
            artistId = None

        return {
            "trackName": songName,
            "trackUrl": trackUrl,
            "albumUrl": albumLink,
            "albumId": albumId,
            "artistUrl": artistLink,
            "artistId": artistId,
            "artistName": artistName,
            "trackId": trackId
        }

    def current_playback(self):
        trackInfo = self.getCurrentTrackData()
        return(super().current_playback(
            SongID=trackInfo["trackUrl"],
            songName=trackInfo["trackName"],
            PlaylistId=trackInfo["albumId"],
            ArtistId=trackInfo["artistId"],
            artistsName=trackInfo["artistName"],
            AlbumID=trackInfo["trackId"]
        ))


if __name__ == "__main__":
    with open("secrets.json") as f:
        secrets = json.load(f)
        username = secrets["spotify"]["username"]
        password = secrets["spotify"]["password"]

    sp = Spotify(username, password, stealth=False)
    driver = sp.driver
    self = sp            #< enables copy pasting from class to pysole

    try:
        import pysole
        pysole.probe()
    except:
        print("Pysole is not installed, for an interactive debugging session, please instal pysole using\npip install liveConsole")