import sqlite3


def _select(table: str, key: str ="", value: str =""):
    u"""Helper funkcija, ki požene sql. Ne je klicati, če ne veš, kaj delaš!"""
    conn = sqlite3.connect("baza.db")
    curs = conn.cursor()
    if not key or not value:
        return curs.execute("SELECT * FROM {}".format(table))

    else:
        if key[0] != '"': key = '"' + key
        if key[-1] != '"': key = key + '"'
        return curs.execute("SELECT * FROM {} WHERE ?=?".format(table), (key, value))

    
def get_elementi():
    u"""Funkcija vrne seznam elementov iz baze"""
    return _select("elementi")
