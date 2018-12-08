import string

def stevilo_velikih(s: str):
    """Prešteje velike črke v stringu"""
    if type(s) != str:
        raise ValueError("s mora biti tipa string")

    count = 0

    for ch in s:
        if ch in string.ascii_uppercase:
            count += 1
    return count
