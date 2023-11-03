from typing import Optional, List
import logging
from .providers import NetEase, Megalobiz, Musixmatch, Lrclib
from .utils import is_lrc_valid

logger = logging.getLogger(__name__)

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
        logger.debug(f"Looking for an LRC on {provider.__class__.__name__}")
        lrc = provider.get_lrc(search_term)
        if is_lrc_valid(lrc, allow_plain_format):
            logger.info(
                f'synced-lyrics found for "{search_term}" on {provider.__class__.__name__}'
            )
            break
    if not lrc:
        logger.info(f'No synced-lyrics found for "{search_term}" :(')
        return
    return lrc
