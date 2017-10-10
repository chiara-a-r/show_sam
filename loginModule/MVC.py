# No use right now but there might be some code can be used later #
# By Wendy on 30 Sep #

from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from model import User
from server import app,login_manager
import sqlite3
"""
    USER table, ENROLLMENT table, COURSE_OFFERING table
    """
users = {'admin':'password'}

class Controller(object):
	def __init__(self):
		pass
	
	def check_password(self, userID, password):
		if userID = 'admin':
			if password == users[admin]:
				return True
		else:
			model = SurveyModel()
			user_info = model.search_userinfo(userID)
			db_password = user_info[0]
			if password == db_password:
				return True
    	return False

	def verify_user(self, userID):
		if self.check_password(userID, password) == False: 
			return view.incorrect_credentials()

		if userID = 'admin':
			return view.admin_dashboard()

		model = SurveyModel()
		view = SurveyView()
		user_info = model.search_userinfo(userID)
		role = user_info[1]

		if role = 'student':
			return view.student_dashboard()
		if role = 'staff':
			return view.staff_dashboard()
		
        

    def search_enrollment(self, userID):
    	model = SurveyModel()
    	view = SurveyView()
    	enrollment = model.search_enrollment()
    	return enrollment

    def search_course_offering(self, sem):
    	model = SurveyModel()
    	view = SurveyView()
    	course_offering = model.search_course_offering()
    	return course_offering


class SurveyModel(object):
	def search_userinfo(self, userID):
		query = "SELECT password, role from USER where userID = '%s' " % userID
		user_info = self.dbselect(query)
		return user_info

	def search_enrollment(self, user_ID):
		pass
	def search_course_offering(sem):
		pass

	def dbselect(self, query):
		connection = sqlite3.connect('survey.db')
        cursorObj = connection.cursor()
        # execute the query
        rows = cursorObj.execute(query)
        connection.commit()
        results = []
        for row in rows:
            results.append(row)
        cursorObj.close()
        return results

class SurveyView(object):
	def incorrect_credentials(self):
		return render_template('login.html', error = 1)
	def student_dashboard(self, userID):
		return render_template('student_dashboard.html', userID = userID)
	def staff_dashboard(self, userID):
		return render_template('staff_dashboard.html', userID = userID)
	def admin_dashboard(self):
		return render_template('admin_dashboard.html')
	 


