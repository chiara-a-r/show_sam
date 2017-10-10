# Use this to write the enrollements.csv into the databse #
# By Wendy on 30 Sep #

import sqlite3
import csv

def write_enrollment_table():
	conn = sqlite3.connect('survey.db')
	cursorObj = conn.cursor()
	create_table_ENROLLMENT = "CREATE TABLE IF NOT EXISTS ENROLLMENT (zID integer FOREIGN KEY, courseCode text FOREIGN KEY, courseTime text FOREIGN KEY)"
	cursorObj.execute(create_table_ENROLLMENT)
	conn.commit()
	with open('enrollments.csv','r') as csv_in:
		reader = csv.reader(csv_in)
		for row in reader:
			sql = "INSERT INTO ENROLLMENT(zID,courseCode,courseTime) VALUES('%s','%s','%s')" %row[0] %row[1] %row[2]
			cursorObj.execute(sql)
			conn.commit()
	cursorObj.close()
	
write_enrollment_table()