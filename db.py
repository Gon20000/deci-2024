import sqlite3

con = sqlite3.connect("main.db")


def read_sql(filename):
    with open(filename) as f:
        return f.read()


def init():
    cur = con.cursor()
    cmds = read_sql("init.sql")
    cur.executescript(cmds)
    cur.close()
    return con


def getLastID(table_name, cur):
    cur.execute(f"SELECT MAX(id) FROM {table_name}")
    return cur.fetchone()[0]


def getLast(table_name, cur=None):
    newCur = cur
    if not newCur:
        newCur = con.cursor()

    last_row_id = getLastID(table_name, newCur)
    newCur.execute(f"SELECT * FROM {table_name} WHERE id = ?", (last_row_id,))

    res = newCur.fetchone()
    if not cur:
        newCur.close()

    return res


def selectRecord(coaching, id):
    table_name = "coaches" if coaching else "athletes"

    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table_name} WHERE id = ?", (id, ))
    res = cur.fetchone()

    cur.close()
    return res


def addAthlete(data):
    cur = con.cursor()
    cur.execute("""INSERT INTO athletes (name, age, gender, club, sport)
                VALUES (?, ?, ?, ?, ?)""", tuple(data))
    con.commit()

    res = getLast("athletes", cur)
    cur.close()

    return res


def addCoach(data):
    cur = con.cursor()
    cur.execute("""INSERT INTO coaches (name, age, gender, price, experience)
                VALUES (?, ?, ?, ?, ?)""", tuple(data))
    con.commit()

    res = getLast("coaches", cur)
    cur.close()

    return res


def sessionExists(date, id, cur):
    cur.execute(
        "SELECT * FROM availability WHERE coachID = ? AND available_date = ?",
        (id, date))
    record = cur.fetchone()

    return record is not None


def addSession(date, id):
    cur = con.cursor()

    exists = sessionExists(date, id, cur)
    if not exists:
        cur.execute(
            "INSERT INTO availability (coachID, available_date) VALUES (?, ?)",
            (id, date))
        con.commit()

    cur.close()

    return not exists


def removeSession(date, id):
    cur = con.cursor()

    exists = sessionExists(date, id, cur)
    if exists:
        cur.execute(
            "DELETE FROM availability WHERE coachID = ? AND available_date= ?",
            (id, date))
        con.commit()

    cur.close()

    return exists
