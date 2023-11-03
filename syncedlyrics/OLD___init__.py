from . import NetEase, Megalobiz, Musixmatch, Lrclib

def search(
    search_term: str,
    musixmatch_cache_location: str):
    _providers = [Lrclib(), Musixmatch(musixmatch_cache_location), Megalobiz(), NetEase()]
    lrc = None
    for provider in _providers:
        lrc = provider.get_lrc(search_term)
        if not ("[" in lrc and "]" in lrc):
            break
    if not lrc:
        return
    return lrc
