import dbus
import hashlib
import os
from lyricsgenius import Genius

class Player:
    def __init__(self):
        self.bus = dbus.SessionBus()
    def _get(self, player, key):
        return player.Get('org.mpris.MediaPlayer2.Player', key, dbus_interface='org.freedesktop.DBus.Properties')
    def _get_playing_player(self):
        for service in self.bus.list_names():
            if service.startswith('org.mpris.MediaPlayer2.'):
                player = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
                status = self._get(player, "PlaybackStatus")
                if status == "Playing":
                    return player
    def get_track_info(self, player=None):
        if player == None:
            player = self._get_playing_player()
        metadata = self._get(player, "Metadata")
        return (metadata['xesam:title'], metadata['xesam:artist'][0])
    def get_track_position(self, player=None):
        if player == None:
            player = self._get_playing_player()
        position = int(self._get(player, "Position"))/10e5
        return round(position, 2)

class LyricsFetcher:
    def __init__(self, genius_api_token, cache_location):
        self.genius = Genius(genius_api_token)
        self.genius.verbose = False
        self.cache_location = cache_location
    def _hash_track(self, track_title, track_artist):
        return hashlib.md5((track_title+track_artist).encode()).hexdigest()
    def fetch_plain(self, track_title, track_artist):
        track_hash = self._hash_track(track_title, track_artist)
        if os.path.isfile(self.cache_location+track_hash+".txt"):
            with open(self.cache_location+track_hash+".txt") as f:
                lyrics = f.read()
            return lyrics, True
        track = self.genius.search_song(track_title, track_artist)
        if track == None:
            return None, False
        lyrics = f"[{track_title} - {track_artist}]\n\n"+"\n".join(track.lyrics.split("\n")[1:])
        if os.path.isdir(self.cache_location) == False:
            os.mkdir(self.cache_location)
        with open(self.cache_location+track_hash+".txt", "w") as f:
            f.write(lyrics)
        return lyrics, True