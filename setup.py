import toml
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from lyricsgenius import Genius
import os
import pwd

CWD = os.getcwd()

unit_service = f"""[Unit]
Description=LyricOverlay

[Service]
WorkingDirectory={CWD}/
ExecStart={CWD}/.venv/bin/python3 main.py
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""

with open("config.toml.sample") as f:
    config = toml.loads(f.read())

print("\nWelcome to [LyricOverlay] installer!\n")

def take_input(text):
    return input(text+"\n> ")

# spotify_client_id = take_input("Please enter your Spotify client ID.")
# spotify_client_secret = take_input("Please enter your Spotify client secret.")

# print("You will now be prompted to log in with your Spotify account.")
# print("Press ENTER to proceed...")
# input()

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=spotify_client_id,
#     client_secret=spotify_client_secret,
#     redirect_uri=config['api']['spotify_redirect_uri'],
#     scope="user-read-currently-playing",
#     cache_handler=CacheFileHandler(cache_path=".spotify_token")))

# print("Testing Spotify...")
# username = sp.current_user()['display_name']
# current_track = sp.current_user_playing_track()
# print(f"Logged in as {username}.")
# if current_track == None:
#     print("Not listening to any track.")
# else:
#     print(f"Listening to {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")
# print()

genius_api_token = take_input("Please enter your Genius API token.")
genius = Genius(config['api']['genius_api_token'])
genius.verbose = False
genius.search_song("Boulevard of Broken Dreams", "Green Day")
print("Genius API functioning.\n")

print("Saving configuration file config.toml...")
# config['api']['spotify_client_id'] = spotify_client_id
# config['api']['spotify_client_secret'] = spotify_client_secret
config['api']['genius_api_token'] = genius_api_token

with open("config.toml", "w") as f:
    f.write(toml.dumps(config))

with open(".unit_service", "w") as f:
    f.write(unit_service)

print("Setup complete.")