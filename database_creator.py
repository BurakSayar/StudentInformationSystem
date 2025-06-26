import csv

from database import Database


obs_students_database = Database('obs', 'students_credentials')
obs_academicians_database = Database('obs', 'academicians_credentials')
obs_students_grades = Database('obs', 'students_grades')


def read_credentials_from_csv(file_path):
    credentials = []
    print('test')
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials.append({"id": row['id'], "mail": row['mail'], "password": row['password']})
    return credentials



credentials = read_credentials_from_csv('credentials.csv')

for credential in credentials:
    sql = "INSERT INTO students_credentials (id, mail, password) VALUES (%s, %s, %s)"
    val = (credential['id'], credential['mail'], credential['password'])
    obs_academicians_database.cursor.execute(sql, val)
    obs_academicians_database.db.commit()
