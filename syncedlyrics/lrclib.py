from typing import Optional
from .base import LRCProvider
import requests

class Lrclib(LRCProvider):
    ROOT_URL = "https://lrclib.net"
    API_ENDPOINT = ROOT_URL + "/api"
    SEARCH_ENDPOINT = API_ENDPOINT + "/search"
    LRC_ENDPOINT = API_ENDPOINT + "/get"

    def __init__(self) -> None:
        self.session.headers.update({
            "User-Agent": f"LYRIC_OVERLAY v0.x (https://github.com/bugbrekr/lyric_overlay)"
        })
        super().__init__()

    def get_lrc(self, search_term: str) -> Optional[str]:
        url = self.SEARCH_ENDPOINT
        r = requests.get(url, params={"q": search_term})
        if not r.ok:
            return
        tracks = r.json()
        if not tracks:
            return
        return tracks[0]['syncedLyrics']