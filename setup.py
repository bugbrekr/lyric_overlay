import toml
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
# from lyricsgenius import Genius
import os
import secrets
import pwd

CWD = os.getcwd()

OUT_CONFIG_FILE_LOCATION = os.path.expanduser("~/.config/lyric_overlay.toml")

if os.path.isfile("config.toml"):
    # upgrading from version v1.8
    IN_CONFIG_FILE_LOCATION = "config.toml"
elif os.path.isfile(OUT_CONFIG_FILE_LOCATION):
    # any update after version v.18
    IN_CONFIG_FILE_LOCATION = OUT_CONFIG_FILE_LOCATION
else:
    # fresh install
    IN_CONFIG_FILE_LOCATION = "config.toml.sample"

with open(IN_CONFIG_FILE_LOCATION) as f:
        config = toml.loads(f.read())

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

# if config['api'].get("genius_api_token") == "XXXXX":
#     genius_api_token = take_input("Please enter your Genius API token.")
#     genius = Genius(config['api']['genius_api_token'])
#     genius.verbose = False
#     genius.search_song("Boulevard of Broken Dreams", "Green Day")
#     print("Genius API functioning.\n")

#     print("Saving configuration file config.toml...")
#     # config['api']['spotify_client_id'] = spotify_client_id
#     # config['api']['spotify_client_secret'] = spotify_client_secret
config['api']['genius_api_token'] = secrets.token_hex(16)

with open(OUT_CONFIG_FILE_LOCATION, "w") as f:
    f.write(toml.dumps(config))

print("Generating service unit...")

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

with open(".unit_service", "w") as f:
    f.write(unit_service)