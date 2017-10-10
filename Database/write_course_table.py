# Use this to write the course.csv into the databse #
# By Wendy on 30 Sep #

import sqlite3
import csv

def write_course_table():
	conn = sqlite3.connect('./sqlite3/survey.db')
	cursorObj = conn.cursor()
	create_table_COURSES = "CREATE TABLE IF NOT EXISTS COURSES (courseCode text PRIMARY KEY, courseTime text PRIMARY KEY)"
	cursorObj.execute(create_table_COURSES)
	conn.commit()
	with open('courses.csv','r') as csv_in:
		reader = csv.reader(csv_in)
		for row in reader:
			sql = "INSERT INTO COURSES(courseCode,courseTime) VALUES('%s','%s')" %row[0] %row[1]
			cursorObj.execute(sql)
			conn.commit()
	cursorObj.close()

write_course_table()