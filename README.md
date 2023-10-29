# Lyric Overlay
Display lyrics for the song you're listening with the press of a button.
Any song. Anytime. Anywhere.

Built for Linux. Tested on Ubuntu (Xfce).

### Technologies Used
 - **Genius**: Web API for fetching lyrics for almost any song.
 - **DBus**: Library to track currently playing music.
 - **Tkinter**: A good GUI framework.

## Compatibility
Built and tested only for Debian based systems including Ubuntu.
The installer uses `systemd`.

## Installation
Please check the [compatibility](#compatibility) of your system before installing.

Obtain an API token from Genius at their [API Client management Page](https://genius.com/api-clients).
### Linux (Debian based)
```
$ wget -qO- https://git.bugbrekr.dev/bugbrekr/lyric_overlay/archive/v1.6.tar.gz | tar xvz
$ cd lyric_overlay/ 
$ ./install.sh
```
OR
```
$ wget -qO- https://git.bugbrekr.dev/bugbrekr/lyric_overlay/archive/v1.6.tar.gz | tar xvz && cd lyric_overlay/ && ./install.sh
```

This will setup the configuration file with default settings and will install a systemd unit-service to run on startup.

## Configuration
All the configuration options can be found in `config.toml`.
#### Window
 - `x_offset` and `y-offset` - Initial location of overlay panel on screen
 - `width_percent` and `height_percent` - Size of overlay panel with respect to the screen size
 - `window_opacity` - Adjust transparency of overlay panel

#### Text
 - `font_size` - Font size of lyrics
 - `font_style` - Font style of lyrics

#### Colours
 - `background` - Colour of overlay panel
 - `text` - Colour of text

### Keybinds
 - `show_hide` - Shortcut hotkey for showing or hiding the overlay panel

#### API
 - `genius_api_token` - API token obtained from the [Genius API Client management Page](https://genius.com/api-clients)

## Usage
**Start by playing a song** on any music player that has a D-Bus registration. You can use VLC Media Player, Spotify, Rhythmbox, Parole, etc.\
You could even use it with YouTube (if the title is just the name of the song, which is unlikely).

You can **show or hide the overlay panel** with the default hotkey `CTRL+ALT+K`, which you can change in the keybinds section of `config.toml`.

The **window can be moved** by just dragging it around with the mouse.

_Note: The program uses caching, but still rate limits API requests at 1 fetch per second._