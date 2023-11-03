from typing import Optional, List
import logging
from .providers import NetEase, Megalobiz, Musixmatch, Lrclib
from .utils import is_lrc_valid

def search(
    search_term: str,
    allow_plain_format: bool = False,
    providers: List[str] = None,
) -> Optional[str]:
    _providers = [Lrclib(), Musixmatch(), Megalobiz(), NetEase()]
    if providers:
        _providers = [p for p in _providers if p.__class__.__name__ in providers]
    lrc = None
    for provider in _providers:
        lrc = provider.get_lrc(search_term)
        if is_lrc_valid(lrc, allow_plain_format):
            break
    if not lrc:
        return
    return lrc
