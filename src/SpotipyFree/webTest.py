import requests

BASE_URL = "http://127.0.0.1:5000"

SPOTIFY_TESTS = {
    "artist": ["3Bd1cgCjtCI32PYvDC3ynO"],
    
    "artist_albums": ["3Bd1cgCjtCI32PYvDC3ynO", "single"], 
    
    "playlist_items": ["6lnfkAgnVtNzvj8KScLSkj"],
    
    "track": ["67Hna13dNDkZvBpTXRIaOJ"],
    
    "album": ["4m2880jivSbbyEGAKfITCa"],
    
    "album_tracks": ["4m2880jivSbbyEGAKfITCa"],
    
    "search": ["Blinding Light - Weekend"]
}

def runTests():
    print("Starting API Endpoint Tests...\n")
    
    for endpoint, payload in SPOTIFY_TESTS.items():
        url = f"{BASE_URL}/{endpoint}"
        
        print(f"POST -> {url}")
        print(f"Payload: {payload}")
        
        try:
            response = requests.post(url, json=payload)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                filename = f"{endpoint}.json"
                try:
                    data = response.json()
                    print(str(data)[:1000])
                    # with open(filename, "w", encoding="utf-8") as f:
                    #     json.dump(data, f, indent=4, ensure_ascii=False)
                    # print(f"Saved response to {filename}")
                except ValueError:
                    print("Response wasn't valid JSON.")
            else:
                print(f"Error Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Connection Error: Make sure your Flask app is running!")
            break
            
        print("-" * 60)

if __name__ == "__main__":
    try:
        import pysole  # type: ignore
    except:
        pysole = None
        print("To get an interactive console, do pip install liveConsole")
    pysole.probe(runRemainingCode=True, printStartupCode=True, removeWaterMark=True)
    # runTests()