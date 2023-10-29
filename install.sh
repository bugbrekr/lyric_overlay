echo "Creating virtual environment..."
python3 -m venv .venv

echo "Installing build-essential libdbus-glib-1-dev libgirepository1.0-dev..."
sudo apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev

echo "Installing packages..."
.venv/bin/python3 -m pip install -r requirements.txt

echo "Running setup script..."
.venv/bin/python3 setup.py

echo "Installing service..."
mv .unit_service ~/.config/systemd/user/lyric-overlay.service
systemctl --user daemon-reload
systemctl --user enable lyric-overlay.service
systemctl --user start lyric-overlay.service 