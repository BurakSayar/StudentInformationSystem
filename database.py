import mysql.connector


class Database:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
        self.db = self.db_connect()
        self.cursor = self.db.cursor(buffered=True)

    def db_connect(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database=self.db_name
        )
        return mydb

    def std_login(self, mail, password):
        self.cursor.execute(f"SELECT * FROM students_credentials WHERE mail = %s AND password = %s", (mail, password,))
        account = self.cursor.fetchone()
        self.db.commit()
        return account


    def acd_login(self, mail, password):
        print(self.table_name)
        self.cursor.execute(f"SELECT * FROM academicians_credentials WHERE mail = %s AND password = %s", (mail, password,))
        account = self.cursor.fetchone()
        self.db.commit()
        return account


    def fetch_all_students(self):
        self.cursor.execute(f'SELECT id, mail FROM students_credentials')
        mails = self.cursor.fetchall()
        self.db.commit()
        return mails


    def mail_to_id(self, mail):
        self.cursor.execute(f'SELECT id FROM students_credentials WHERE mail = %s', (mail,))
        id = self.cursor.fetchone()
        self.db.commit()
        return id

    def id_to_grades(self, id):
        self.cursor.execute(f'SELECT * FROM students_grades WHERE id = %s', (id,))
        grades = self.cursor.fetchone()
        self.db.commit()
        return grades


    def update_grade(self, id, alg, spd, ld, ds, os, clc):
        if not self.id_to_grades(id) == None:
            self.cursor.execute(
                'UPDATE students_grades SET alg = %s, spd = %s, ld = %s, ds = %s, os = %s, clc = %s WHERE id = %s',
                (alg, spd, ld, ds, os, clc, id))
            self.db.commit()
            return True
        self.cursor.execute('INSERT INTO students_grades (id, alg, spd, ld, ds, os, clc) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, alg, spd, ld, ds, os, clc,))
        self.db.commit()