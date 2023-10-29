echo "Creating virtual environment..."
python3 -m venv .venv

echo "Installing build-essential libdbus-glib-1-dev libgirepository1.0-dev..."
sudo apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev

echo "Installing packages..."
.venv/bin/python3 -m pip install -r requirements.txt

echo "Running setup script..."
.venv/bin/python3 setup.py

echo "Installing service..."
sudo mv .unit_service /etc/systemd/system/lyric-overlay.service
sudo systemctl daemon-reload
sudo systemctl enable lyric-overlay.service
sudo systemctl start lyric-overlay.service 