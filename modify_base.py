u"""Datoteka se uporablja za urejanje baze podatkov, če strežnik ni vključen"""

import sqlite3
from sys import argv

conn = sqlite3.connect("data.db")
curs = conn.cursor()


def process_array(arr):
    vals = []
    for el in arr:
        try:
            val = int(el)
            val = el
        except ValueError:
            val = "'{}'".format(el)
        vals.append(val)
    return vals


if __name__=="__main__":

    file_open = False
    for arg in argv:
        if arg == "--file":
            file_open = True
        elif file_open and not arg.startswith("-"):
            filename = arg

    if file_open:
        with open(filename) as f:
            table = None
            for i, ln in enumerate(f):
                if ln.startswith("+"):
                    table = ln[1:]
                else:
                    if table is None:
                        print("Error on line {}: No table set for adding into".format(i+1))
                        quit(-1)
                    else:
                        data = ",".join([i]+process_array(ln.split(":")))
                        curs.execute("INSERT INTO {} VALUES ({})".format(table, data))
                        conn.commit()
        quit(0)
    
    cmd = input("> ")
    closed = False

    while cmd != "q" and not closed:

        if cmd.startswith("sql "):
            sql = cmd[4:]
            rvl = curs.execute(sql)
            for l in rvl:
                print(l)

        if cmd.startswith("save"):
            conn.commit()

        if cmd.startswith("cancel"):
            closed = True
            conn.close()

        if cmd.startswith("insert"):
            table = input("table? ")
            data = input("data? ")
            if data[0] != "(":
                data = "(" + data
            if data[-1] != ")":
                data = data + ")"
            curs.execute("INSERT INTO {} VALUES {}".format(table, data))

        if cmd.startswith("select"):
            table = input("table? ")
            a = input("WHERE ? ")
            if a != "":
                b = input("=? ")
                if b[0] != '"': b = '"' + b
                if b[-1] != '"': b = b + '"'
                data = curs.execute("SELECT * FROM {} WHERE {}={}".format(table, a, b))
                for l in data:
                    print(l)
            else:
                data = curs.execute("SELECT * FROM {}".format(table))
                for l in data:
                    print(l)
            

        if closed:
            quit()

        cmd = input("> ")

    if not closed:
        conn.commit()
        conn.close()
