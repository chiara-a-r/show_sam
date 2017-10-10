
from flask import Flask, session, redirect, request, render_template, url_for, current_app
from flask_wtf import Form
from wtforms import SubmitField
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from model import User, authenticateModel
from server import app,login_manager
from functools import wraps
import sqlite3
import csv

#from ExternalDataModel import ExternalDataModel
from InternalDataModel import Survey, InternalDataModel
from authenticate import login_required

dataModel = InternalDataModel()
survey_name = ""
expDate = "10/10/17"

class chooseSessionForm(Form):
    course_chosen = SubmitField()
    session_chosen = SubmitField()


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
                session['user_id'] = zID
                return redirect(url_for("student_dashboard"))
                #intData = InternalDataModel()
                #intData.create_survey(zID, password)
                #all_surveys = intData.get_all_surveys()
                #error = (all_surveys)
        else:
            error = "Your log-in details are incorrect, please try again."
    return render_template("login.html", error = error)


@app.route('/AdminDashboard',methods = ["GET", "POST"])
#@login_required(role="admin")
def admin_dashboard():
    
    expDate = "10/10/17"
    active_surveys = []
    to_be_reviewed_surveys = []
    questions = []
    
    #dataModel.create_survey("COMP1531", expDate)
    #dataModel.update_survey_status("COMP1531", 'Active')
    #dataModel.create_survey("COMP2041", expDate)
    #dataModel.update_survey_status("COMP2041", 'ToBeReviewed')
    
    if request.method == "POST":
        if request.form["close"]:
            dataModel.update_survey_status(request.form.get("close"), "Closed")
        if request.form["remove"]:
            for q in dataModel.get_questions():
                if q.question_text == request.form["remove"]:
                    dataModel.delete_question(q.id)

    for survey in dataModel.get_Active_surveys():
        active_surveys.append(survey.surveyName)
    for survey in dataModel.get_ToBeReviewed_surveys():
        to_be_reviewed_surveys.append(survey.surveyName)
    for question in dataModel.get_questions():
        questions.append(question.question_text)
    return render_template("admin_dashboard.html", live_surveys=active_surveys, surveys_to_review=to_be_reviewed_surveys, questions=questions)

@app.route('/CreateQuestion',methods = ["GET", "POST"])
def create_question():

    if request.method == "POST":
        if request.form.get("addQuestion") == "pressed":
            #intakes all the input by the user
            question = request.form.get("question")
            typeQ = request.form.get("type")
            basis = request.form.get("basis")
            #adds question to database
            dataModel.add_question(question, typeQ, basis)
            return redirect(url_for('question_added'))

    return render_template("create_question.html")

@app.route('/QuestionAdded', methods = ["GET", "POST"])
def question_added():
    if request.method == "POST":
        #if a button is pressed
        if request.form.get("action"):
            #if they clicked 'Add another question'
            if request.form.get("action") == "addQ":
                return render_template("create_question.html")
            #if they clicked 'Return to dashboard'
            else:
                return redirect('admin_dashboard')
    return render_template("questionAdded.html")

@app.route('/ChooseSession', methods = ["GET", "POST"])
def choose_session():
    form = chooseSessionForm()
    
    courses = dataModel.get_all_courseOffering()
    course_sessions = []
    course_codes = []
    for course in courses:
        if course.courseCode not in course_codes:
            course_codes.append(course.courseCode)
    if form.validate_on_submit():
        if form.course_chosen.data:
            course = request.method.get("course")
            for c in dataModel.get_all_courseOffering():
                course_sessions.append(c.courseTime)
            return render_template("choose_session.html", courses=course_codes, sessions=course_sessions)
        if form.session_chosen.data:
            session = request.method.get("session")
            survey_name = course + session
            return redirect('create_survey')
    return render_template("choose_session.html", courses=course_codes, form=form)


@app.route('/CreateSurvey', methods = ["GET", "POST"])
def create_survey():

    finished = 0
    dataModel.add_question("How are you?", "M", "MCQ")
    all_questions = dataModel.get_questions()
    man_questions = []
    man_questions_text = []
    for question in all_questions:
        if question.question_type == "M":
            man_questions.append(question)
            man_questions_text.append(question.question_text)

    if request.method == "POST":
        if request.form.get("create_survey"):
            #gets all the questions selected by checkboxes
            selected_questions_names = request.form.getlist('question')
            selected_questions = []
            finished = 1
            dataModel.create_survey(survey_name, "10/10/17") #example exp date
            #go thru all questions and find selected_questions
            for q in dataModel.get_questions():
                for s in selected_questions_names:
                    if q.question_text == s:
                        selected_questions.append(q)
            for question in selected_questions:
                dataModel.add_question_to_survey(survey_name, question.id)

    return render_template("create_survey.html", man_questions=man_questions_text, finished=finished)

@app.route('/Metrics',methods = ["GET", "POST"])
def metrics():
    closed_surveys = []
    for s in dataModel.get_Closed_surveys():
        if s not in closed_surveys:
            closed_surveys.append(s)
    if request.method == "POST":
        if request.form.get("search"):
            pressed = 1
            survey = request.form.get("survey")
            responses = []
            questions_in_survey = dataModel.get_questions_in_survey()
            for question in questions_in_survey:
                responses.append(get_all_response_for_a_question_in_survey(survey, question.id))
            return render_template("metrics.html", answers=responses, pressed=pressed)
    
    return render_template("metrics.html", surveys=closed_surveys)


@app.route('/StaffDashboard',methods = ["GET", "POST"])
@login_required(role="staff")
def staff_dashboard():
    to_be_reviewed_surveys = []
    optionalQs = []
    staffAccess = InternalDataModel()
    zID = session['user_id']
    staffCourses = staffAccess.search_user_enrollments(zID)

    for survey in staffAccess.get_ToBeReviewed_surveys():
       to_be_reviewed_surveys.append(survey.survey_name)

       if request.form.get("review"):
          return redirect(url_for('review_survey'))
    return render_template("staff_dashboard.html",surveys_to_review=to_be_reviewed_surveys, questions=optionalQs)

@app.route("/<survey_name>_review", methods = ["GET", "POST"])
def add_question():
   if request.form.get("addQuestion"):
       question = request.form.get("question")
       typeQ = request.form.get("type")
       basis = request.form.get("basis")
       newDataModel.add_question(question, typeQ, basis)
       return render_template("question_added.html")
   return render_template("survey_name.html")

def submit_survey():
   if request.form.get("finalise"):
      active_surveys.append(survey.survey_name)
      to_be_reviewed_surveys.remove(survey.survey_name)
      return render_template("survey_complete.html")
   return render_template("review_survey.html")

@app.route('/StudentDashboard',methods = ["GET", "POST"])
@login_required(role="student")
def student_dashboard():
    course_surveys = []
    open_surveys_info = []
    closed_survey_info = []

    #get the zID: zID was stored in a session from the login page
    zID = session['user_id']
    expDate = "10/10/17"

    # get all the courses the student is enrolled in
    #studEnrol = ExternalDataModel() # ExternalDataModel is the class name from the file ExternalDataModel.py
    studEnrol = InternalDataModel()
    enrollments = studEnrol.search_user_enrollments(zID) # returned a list of tuples e.g. [(COMP1531, 17S2), ...]

    #FOR TESTING
    # create the survey
    # this is wrong in the sense that it will make it again even if the survey name exists.. This is Chiara's part right? IDEK
    studEnrol.create_survey("COMP1531", expDate)
    studEnrol.create_survey("COMP2041", expDate)

    # update the status
    studEnrol.update_survey_status("COMP2041", "active")
    studEnrol.update_survey_status("COMP1531", "closed")
    studEnrol.update_survey_status("100", "closed")


    # get all the surveys ?
    all_surveys = studEnrol.get_all_surveys()


    for i in enrollments :
    # get all the surveys in that course
    # According to Chiara (creating the surveys), the name of the survey should be like the tuple above
        # for each in all_surveys :
            # if each == Survey.surveyName
            course_surveys.append(Survey) # Survey is from InternalDataModel->class Survey

    # get if they are still open or closed
    #for surv in course_surveys :
    for surv in all_surveys :
        if surv.status == "active" :
            surv_info = (surv.surveyName, surv.ExpiryDate)
            open_surveys_info.append(surv_info)
            # open_surveys_info.append(surv.surveyName)
            # open_surveys_info.append(surv.ExpiryDate)
            # GET THE URL OF THE SURVEY AS WELL
        elif surv.status == "closed" :
            closed_survey_info.append(surv.surveyName)
            closed_survey_info.append(surv.ExpiryDate)
            # GET THE URL OF THE SURVEY AS WELL

    return render_template("student_dashboard.html", stu_enrollments = enrollments, all_surveys = all_surveys, course_surveys = course_surveys, open_surveys = open_surveys_info, closed_surveys = closed_survey_info )

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    logout_user()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
