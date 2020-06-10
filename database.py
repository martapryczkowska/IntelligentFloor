import sqlite3
import contextlib

class Database:
    def __init__(self, name):
        self.name = name
        self.create_tables()

    def create_tables(self):
        with contextlib.closing(sqlite3.connect(self.name)) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS patient (idPatient INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, surname TEXT NOT NULL, age INTEGER)')
            cur.execute('CREATE TABLE IF NOT EXISTS measurement (patientId INTEGER PRIMARY KEY, defect TEXT, FOREIGN KEY (patientId) REFERENCES patient (idPatient))')
            conn.commit()

    def data_entry(self, name, lastName, age, defect):

        with contextlib.closing(sqlite3.connect(self.name)) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO patient(name, surname, age) VALUES (?, ?, ?)",
                             (name, lastName, age))
            id = cur.lastrowid
            conn.commit()

        if id is None:
            id = 0
        with contextlib.closing(sqlite3.connect(self.name)) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO measurement(patientId, defect) VALUES (?, ?)",
                                                                        (id, defect))
            conn.commit()

    def data_search(self, name, lastname):

        result = []
        with contextlib.closing(sqlite3.connect(self.name)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT idPatient, name, surname, age FROM patient WHERE name=? AND surname=?", (name,lastname))
            datas = cur.fetchall()
            if not datas:
                return None

        for data in datas:
            (f_idPatient, f_name, f_surname, f_age) = data
            result.append([f_idPatient, f_name, f_surname, f_age])

        for record in result:
            with contextlib.closing(sqlite3.connect(self.name)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT defect FROM measurement WHERE patientId=?",(record[0],))
                defects = cur.fetchall()
                for defect in defects:
                    (f_defect,) = defect
                    record.append(f_defect)

        for record in result:
            if len(record)!=5:
                result.remove(record)

        return result
