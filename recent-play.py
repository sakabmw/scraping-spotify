from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

# Spotify Credentials
# The variables will pick their respective values from .env
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Check point whether the CLIENT_ID or CLIENT_SECRET is already set or not
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Please set the SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")

# Set up Spotipy authorization
scope = "user-read-recently-played"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope))

# Fetch recently played tracks, allowed to only <= 50 songs
# The results are json formatted data
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
        duration_m = track['duration_ms']/1000/60 # convert miliseconds to minutes
        
        # Append a dictionary to the playback_data list
        playback_data.append({
            'track_name': track_name,
            'artists': artists,
            'album_name': album_name,
            'album_art_url': album_art_url,
            'played_at': played_at,
            'spotify_url': spotify_url,
            'duration_m': duration_m
        })
    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(playback_data)

    # Convert 'played_at' to datetime for easier manipulation
    df['played_at'] = pd.to_datetime(df['played_at'])

    # Add `date part only` version of `played_at`
    df['played_at_date'] = pd.to_datetime(df['played_at'].dt.date)
    
    return df

# Store the results data in a pandas dataframe
df = parse_recent_playback(results)

def data_agg(df):
    """
    This funcion will show the aggregated data of the parsing results

    Args:
        df (pd.DataFrame): A DataFrame with columns for track details and playback time.

    Returns:
        pd.DataFrame: An aggregated table from the input, showing the number of albums and tracks from each artist.
    """

    df_agg = df.groupby('artists').agg(
        num_album = ('album_name', 'nunique'),
        num_track = ('track_name', 'nunique'),
        total_minutes = ('duration_m', 'sum'),
        max_played_date = ('played_at_date', 'max'),
        min_played_date = ('played_at_date', 'min')
    ).sort_values(
        ['num_album', 'num_track'],
        ascending=False)
    
    df_agg = print(df_agg)

    return df_agg

# Run function `data_agg()` to retrieve the aggregated data and
# store the raw results data in a CSV file
if __name__ == '__main__':
    filename = 'spotify_recent_playback.csv'

    print('\n======Start aggregating data======\n')
    data_agg(df)
    print('\n======Finish aggregating data======\n')
    
    print('======Start storing results into a CSV file======\n')
    df.to_csv(filename, index=False)
    print('======Finish creating the CSV file, named as {}======\n'.format(filename))
else:
    None