printf "\nWelcome to [LyricOverlay] installer!\n\n"

echo "Creating virtual environment..."
python3 -m venv .venv

if ! dpkg -s build-essential libdbus-glib-1-dev libgirepository1.0-dev; then
    echo "Installing build-essential libdbus-glib-1-dev libgirepository1.0-dev..."
    sudo apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev
fi

echo "Installing packages..."
.venv/bin/python3 -m pip install -r requirements.txt

if ! .venv/bin/python3 setup.py; then
    echo "And error has occurred."
    exit 1
fi

echo "Installing service..."
mv .unit_service ~/.config/systemd/user/lyric-overlay.service
systemctl --user daemon-reload
systemctl --user enable lyric-overlay.service
systemctl --user start lyric-overlay.service 