u"""Datoteka se uporablja za urejanje baze podatkov, če strežnik ni vključen"""

import sqlite3

conn = sqlite3.connect("data.db")
curs = conn.cursor()


if __name__=="__main__":
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
