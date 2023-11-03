import toml
import os
import secrets

CWD = os.getcwd()


os.mkdir(os.path.expanduser("~/.config/"))
os.mkdir(os.path.expanduser("~/.cache/"))
os.mkdir(os.path.expanduser("~/.cache/lyric_overlay/"))
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