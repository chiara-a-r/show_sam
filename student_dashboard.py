from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list, survey_name, n
import csv

from ExternalDataModel import ExternalDataModel
from InternalDataModel import Survey
#from authenticate import login_required

@app.route('/StudentDashboard',methods = ["GET", "POST"])
#@login_required(role="student")
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

    return render_template("student_dashboard.html", open_surveys = open_surveys_info, closed_surveys = closed_survey_info )

#class ExternalDataModel(object):
#    def search_user_enrollments(self,zID):
#        query = "SELECT courseCode, courseTime from ENROLLMENT where zID = '%s' " %zID
#        enrollments = self.dbselect(query)
#        return enrollments # it is a list of tuples, e.g. [(COMP1531,17S2),(COMP2521,17S2)]

#class Survey(Base):
#    __tablename__ = 'SURVEY'
#    surveyName = Column(String, primary_key=True, nullable=False) # survey name
#    status = Column(String, nullable=False) # active, toBeReviewed, closed
#    ExpiryDate = Column(String)

#    def __repr__(self):
#        return "[Survey: '%s', Status = '%s', ExpiryDate = '%s']" %(self.surveyName, self.status, self.ExpiryDate)

# Need to send details of COURSES the student takes, due date
# Send them all over, and inside the html folder, only show it if the student hasnt done that survey yet..
    # Then have to return if they've completed it?

"""
1. can see enrolled and active surveys
2. click on the survey links and can fill in the survey
"""
