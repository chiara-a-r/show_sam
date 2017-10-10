# Use this to write the passwords.csv and add the admin as well into the databse #
# By Wendy on 30 Sep #

import sqlite3
import csv

def write_user_table():
    conn = sqlite3.connect('SurveySystem.db')
    cursorObj = conn.cursor()
    create_table_USER = "CREATE TABLE IF NOT EXISTS USER (zID text PRIMARY KEY, password text NOT NULL, role text NOT NULL)"
    cursorObj.execute(create_table_USER)
    conn.commit()
    insert_admin = "INSERT INTO USER(zID,password,role) VALUES('adminID','admin_password','admin')"
    cursorObj.execute(insert_admin)
    conn.commit()
    with open('passwords.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            sql = "INSERT INTO USER(zID,password,role) VALUES(?,?,?)"
            cursorObj.execute(sql,(row[0], row[1], row[2]))
            conn.commit()
    cursorObj.close()

write_user_table()
