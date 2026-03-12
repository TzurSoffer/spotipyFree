# Selenium-Spotify

A lightweight **drop-in replacement for Spotipy** that uses **Selenium** to control and read data from the Spotify Web Player.

This project mimics parts of the **Spotify Web API** without requiring developer credentials or the official API. Instead, it logs into the Spotify web player and scrapes playback information.

Currently the library focuses on **retrieving the current playback state** in a format compatible with the Spotify API.

- - -

## Features

*   Drop-in style response compatible with `spotipy.current_playback()`
    
*   No Spotify developer account required
    
*   Works directly with the Spotify Web Player
    
*   Simple login using username and password
    
*   Returns playback data structured like the official Spotify API
    

- - -

## Current Status

⚠️ This project is **experimental**.

Currently implemented:

*   `current_playback()`  
    Returns playback information similar to the Spotify Web API.
    

Limitations:

*   Only the **currently playing track** is supported
    
*   Some page loads rely on DOM scraping and may break if Spotify updates their UI
    
*   Occasionally **Spotify CAPTCHA** may appear during login
    
*   Performance is slower than the official API due to browser automation
    

- - -

## Installation

Bash

pip install selenium

You must also install **ChromeDriver** compatible with your Chrome version.

- - -

## Usage

Python

Run

from selenium\_spotify import Spotify  
  
sp \= Spotify("username", "password")  
  
playback \= sp.current\_playback()  
print(playback\["item"\]\["name"\])

Example response structure (compatible with Spotipy):

Python

Run

playback\["item"\]\["name"\]  
playback\["item"\]\["artists"\]\[0\]\["name"\]  
playback\["item"\]\["album"\]\["name"\]

- - -

## Secrets File Example

The included example expects a `secrets.json` file:

JSON

{  
  "spotify": {  
    "username": "your\_username",  
    "password": "your\_password"  
  }  
}

- - -

## How It Works

1.  Selenium logs into `accounts.spotify.com`
    
2.  The web player is opened
    
3.  The script navigates to the **queue page**
    
4.  Track metadata is extracted from the DOM
    
5.  A response object is generated matching the **Spotify Web API format**
    

- - -

## Known Issues

*   CAPTCHA sometimes appears during login
    
*   Page structure changes from Spotify can break selectors
    
*   Selenium adds noticeable overhead compared to API calls
    
*   Requires a running Chrome browser

*   Code is ugly, I need to fix that...

*  Stealth mode not working
    

- - -

## Planned Improvements

*   Cookie-based login (avoid CAPTCHA and login delays)
    
*   Faster page scraping
    
*   More API compatibility
    
    *   `devices`
        
    *   `playlists`
        
    *   `pause / play`
        
    *   `next / previous`
        
*   Headless mode improvements
    
*   Session persistence
    

- - -

## Warning

This project uses **browser automation** and **unofficial scraping** of the Spotify Web Player.

It is **not affiliated with Spotify** and may break if Spotify changes their website.
