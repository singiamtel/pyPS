import re

def toID(s) -> str:
    # /[^a-z0-9]/g
    if type(s) == str:
        return re.sub(r'[^a-z0-9]', '', s.lower())
    return ''
