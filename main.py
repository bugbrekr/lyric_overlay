import threading
import tkinter as tk
import tkinter.ttk as ttk
import toml
from pynput import keyboard
from pynput.mouse import Controller
import time
import requests
import os
import functions

CONFIG_FILE_LOCATION = os.path.expanduser("~/.config/lyric_overlay.toml")
CACHE_FOLDER_LOCATION = os.path.expanduser("~/.cache/lyric_overlay/")

with open(os.path.expanduser("~/.config/lyric_overlay.toml")) as f:
    config = toml.loads(f.read())

mouse = Controller()

lyrics_fetcher = functions.LyricsFetcher(CACHE_FOLDER_LOCATION)
player = functions.Player()

root = tk.Tk()
root.withdraw()

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
WINDOW_WIDTH_FRACTION = config['window']['width_percent']/100
WINDOW_HEIGHT_FRACTION = config['window']['height_percent']/100
WINDOW_X_OFFSET = config['window']['x_offset']
WINDOW_Y_OFFSET = config['window']['y_offset']
WINDOW_OPACITY = config['window']['window_opacity']/100

KEYBINDS_SHOW_HIDE = config['keybinds']['show_hide']

COLOURS_BACKGROUND = config['colours']['background']
COLOURS_TEXT = config['colours']['text']

TEXT_FONT_SIZE = config['text']['font_size']
TEXT_FONT_STYLE = config['text']['font_style']

WINDOW_WIDTH = int(SCREEN_WIDTH*WINDOW_WIDTH_FRACTION)
WINDOW_HEIGHT = int(SCREEN_HEIGHT*WINDOW_HEIGHT_FRACTION)
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}{WINDOW_X_OFFSET:+}{WINDOW_Y_OFFSET:+}"

style = ttk.Style(root)
style.configure('Text.TFrame', background=COLOURS_BACKGROUND, foreground=COLOURS_BACKGROUND)

style.layout('arrowless.Vertical.TScrollbar', 
         [('Vertical.Scrollbar.trough',
           {'children': [('Vertical.Scrollbar.thumb', 
                          {'expand': '1', 'sticky': 'ns'})],
            'sticky': 'ns'})])

class Window:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Lyric Overlay")
        self.window.geometry(WINDOW_GEOMETRY)
        self.window.attributes('-type', 'dock')
        self.window.attributes("-alpha", WINDOW_OPACITY)
        self.window.config(background=COLOURS_BACKGROUND)
        self.is_shown = False
        self.movable = False
        self.last_api_hit = 0
    def init(self):
        def for_canonical_l(f):
            return lambda k: f(l.canonical(k))
        hotkey = keyboard.HotKey(keyboard.HotKey.parse(KEYBINDS_SHOW_HIDE), self.on_hotkey)
        l = keyboard.Listener(on_press=for_canonical_l(hotkey.press), on_release=for_canonical_l(hotkey.release))
        l.start()
        self._init_window()
        self.is_shown = True
        self.window.bind("<ButtonPress-1>", self.on_mv_down)
        self.window.bind("<ButtonRelease-1>", self.on_mv_up)
        self.window.mainloop()
    def _init_window(self):
        self.txt = tk.Text(self.window, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=1)
        self.txt.config(font=(TEXT_FONT_STYLE, TEXT_FONT_SIZE), background=COLOURS_BACKGROUND, foreground=COLOURS_TEXT)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.update_window()
    def _set_window_text(self, text):
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.INSERT, text)
    def show(self):
        self.update_window()
        self.window.deiconify()
        self.is_shown = True
    def hide(self):
        self.window.withdraw()
        self.is_shown = False
    def _update_window(self):
        track = player.get_track_info()
        if track == None:
            self._set_window_text("No track playing.")
            return
        track_title, track_artist = track
        if time.time()-self.last_api_hit < 1:
            self._set_window_text("Slow down! Try again in a second.")
            return
        self._set_window_text("Searching for lyrics...")
        
        try:
            self.last_api_hit = time.time()
            lyrics_data, res = lyrics_fetcher.fetch_synced(track_title, track_artist)
        except requests.exceptions.Timeout as e:
            self._set_window_text("ERROR: Request timed out.\nTry again.")
            return

        if res == False:
            self._set_window_text("Sorry, lyrics not found.")
            return
        lyrics = lyrics_data['synced_lyrics']
        self._set_window_text(lyrics)
        self.txt.yview("scroll", 5, "units")
    def update_window(self):
        threading.Thread(target=self._update_window).start()
    def on_hotkey(self):
        if self.is_shown:
            self.hide()
        else:
            self.show()
    def _cursor_follow_loop(self):
        self.movable = True
        relx = self.window.winfo_x()-mouse.position[0]
        rely = self.window.winfo_y()-mouse.position[1]
        while self.movable:
            new_x = mouse.position[0]+relx
            new_y = mouse.position[1]+rely
            if new_x+WINDOW_WIDTH >= SCREEN_WIDTH:
                new_x = SCREEN_WIDTH-WINDOW_WIDTH
            if new_y+WINDOW_HEIGHT >= SCREEN_HEIGHT:
                new_y = SCREEN_HEIGHT-WINDOW_HEIGHT
            if new_x <= 0:
                new_x = 0
            if new_y <= 0:
                new_y = 0
            self.window.geometry(f"+{new_x}+{new_y}")
            time.sleep(0.01)
    def on_mv_down(self, event):
        threading.Thread(target=self._cursor_follow_loop).start()
    def on_mv_up(self, event):
        self.movable = False

window_controller = Window(root)
window_controller.init()