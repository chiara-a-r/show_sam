# This file may evolve into a surveyModel #
# By Wendy on 30 Sep #

import sqlite3
from questions import questions, MCQ, TexBQ

def create_survey_table(survey_name):
	conn = sqlite3.connect('./sqlite3/survey.db')
	cursorObj = conn.cursor()
	create_survey_table = "CREATE TABLE IF NOT EXISTS '%s' (question text PRIMARY KEY, type text NOT NULL, based text NOT NULL)" %survey_name
	cursorObj.execute(CREATE_TABLE)
	cursorObj.close()

def insert_question(survey, question, based):
	conn = sqlite3.connect('./sqlite3/survey.db')
	sql = "INSERT INTO '%s' (question, type, based) VALUES('%s','%s','%s')" %survey %question.get_question() %question.get_type() %based
	cursorObj = conn.cursor()
	cursorObj.execute(sql)
	cursorObj.close()

def delete_question(survey, question):
	conn = sqlite3.connect('./sqlite3/survey.db')
	sql = "DELETE FROM '%s' WHERE question ='%s'" %survey %question
	cursorObj = conn.cursor()
	cursorObj.execute(sql)
	cursorObj.close()

def delete_all_question():
	conn = sqlite3.connect('./sqlite3/survey.db')
	sql = "DELETE FROM '%s'" %survey
	cursorObj = conn.cursor()
	cursorObj.execute(sql)
	cursorObj.close()
 
def select_question(survey, condn):
	conn = sqlite3.connect('./sqlite3/survey.db')
	sql = "SELECT * from '%s' where '%s' " %survey %condn
	cursorObj = conn.cursor()
	rows = cursorObj.execute(sql)
	results = []
	for row in rows:
		results.append(row)
	cursorObj.close()
	return results