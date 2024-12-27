from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

load_dotenv()

# Retrieve Client ID and Client Secret
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Please set the SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")

# Authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Example: Search for a track
track_name = "Blinding Lights"
results = sp.search(
    q=track_name,
    limit=1,
    type='track')

# Print track details
if results['tracks']['items']:
    track = results['tracks']['items'][0]
    print(f"Track Name: {track['name']}")
    print(f"Artist: {track['artists'][0]['name']}")
    print(f"Album: {track['album']['name']}")
    print(f"Release Date: {track['album']['release_date']}")
    print(f"Preview URL: {track['preview_url']}")
else:
    print("Track not found.")