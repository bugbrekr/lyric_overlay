from bs4 import BeautifulSoup, FeatureNotFound

def is_lrc_valid(lrc: str, allow_plain_format: bool = False) -> bool:
    if not lrc:
        return False
    if not allow_plain_format:
        if not ("[" in lrc and "]" in lrc):
            return False
    return True

def generate_bs4_soup(session, url: str, **kwargs):
    r = session.get(url)
    try:
        soup = BeautifulSoup(r.text, features="lxml", **kwargs)
    except FeatureNotFound:
        soup = BeautifulSoup(r.text, features="html.parser", **kwargs)
    return soup