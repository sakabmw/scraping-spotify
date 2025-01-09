from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

# Spotify Credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
APP_REDIRECT_URI = os.getenv("APP_REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Please set the SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")

# Set up Spotipy authorization
scope = "user-read-recently-played"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=APP_REDIRECT_URI,
        scope=scope))

# Fetch recently played tracks
results = sp.current_user_recently_played(limit=50)

def parse_recent_playback(results):
    """
    Parses Spotify recent playback data into a pandas DataFrame.

    Args:
        results (dict): The JSON response from Spotify's "recently played" API.

    Returns:
        pd.DataFrame: A DataFrame with columns for track details and playback time.
    """
    # Initialize an empty list to store parsed data
    playback_data = []

    # Loop through each playback item in the results
    for item in results['items']:
        track = item['track']
        
        # Extract necessary details
        track_name = track['name']
        artists = ", ".join(artist['name'] for artist in track['artists'])  # Multiple artists joined by commas
        album_name = track['album']['name']
        album_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None
        played_at = item['played_at']
        spotify_url = track['external_urls']['spotify']
        
        # Append a dictionary to the playback_data list
        playback_data.append({
            'track_name': track_name,
            'artists': artists,
            'album_name': album_name,
            'album_art_url': album_art_url,
            'played_at': played_at,
            'spotify_url': spotify_url
        })
    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(playback_data)

    # Convert 'Played At' to datetime for easier manipulation
    df['played_at'] = pd.to_datetime(df['played_at'])
    
    return df

# Retrieve the results in a dataframe
df = parse_recent_playback(results)
print(df.head())
print(df[['album_name', 'artists']].head())
print(df.info())
df_unique = df.groupby('album_name')['track_name'].nunique().sort_values(ascending=False)
print(df_unique)