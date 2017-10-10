# Login module #
# By Wendy on 30 Sep #

from flask import Flask, redirect, request, render_template, url_for, current_app
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from model import User, authenticateModel
from server import app,login_manager, question_list, survey_name, n
from functools import wraps
import sqlite3
import csv

from ExternalDataModel import ExternalDataModel
from InternalDataModel import Survey
from authenticate import login_required

def check_password(zID, password):
    model = authenticateModel()
    if model.search_detail(zID) == []:
        return False
    user_detail = model.search_detail(zID)[0]
    user_dbpsw = user_detail[0]
    if password == user_dbpsw:
        user =  User(zID, user_detail[0], user_detail[1]) # should there be zID only?
        login_user(user)
        return True
    return False

def get_user(zID):
    model = authenticateModel()
    user_detail = model.search_detail(zID)[0]
    password = user_detail[0]
    role = user_detail[1]
    return User(zID, user_detail[0],user_detail[1])

@login_manager.user_loader
def load_user(zID):
    user = get_user(zID)
    return user

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if ( (current_user.role != role) and (role != "ANY")):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/',methods=["GET","POST"])
def login():
    error = ''
    if request.method == "POST":
        zID = request.form["zID"]
        password = request.form["password"]
        if check_password(zID, password):
            if current_user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif current_user.role == "staff":
                return redirect(url_for("staff_dashboard"))
            elif current_user.role == "student":
                return redirect(url_for("student_dashboard"))
        else:
            error = "Your log-in details are incorrect, please try again."
    return render_template("login.html", error = error)

#@app.route('/AdminDashboard',methods = ["GET", "POST"])
#@login_required(role="admin")
#def admin_dashboard():
#    return render_template("admin_dashboard.html")

#@app.route('/StaffDashboard',methods = ["GET", "POST"])
#@login_required(role="staff")
#def staff_dashboard():
#    return render_template("staff_dashboard.html")

@app.route('/StudentDashboard',methods = ["GET", "POST"])
@login_required(role="student")
def student_dashboard():
    course_surveys = []
    open_surveys_info = []
    closed_survey_info = []

    # get all the courses the student is enrolled in
    studEnrol = ExternalDataModel() #ExternalDataModel is the class name
    enrollments = studEnrol.search_user_enrollments(zID) # returned a list of tuples e.g. [(COMP1531, 17S2), ...]

    for i in enrollments :

    # get all the surveys in that course
    course_surveys.append(Survey)

    # get if they are still open or closed
    for surveys in course_surveys :
        if surveys.status == "active" :
            open_surveys_info.append(surveys.surveyName)
            open_surveys_info.append(surveys.ExpiryDate)
            # GET THE URL OF THE SURVEY AS WELL
        elif surveys.status == "closed" :
            closed_survey_info.append(surveys.surveyName)
            closed_survey_info.append(surveys.ExpiryDate)
            # GET THE URL OF THE SURVEY AS WELL

    return render_template("student_dashboard.html", stu_enrollments = enrollments, open_surveys = open_surveys_info, closed_surveys = closed_survey_info )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
