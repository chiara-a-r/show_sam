# use Python3 and sqlalchemy to implement the InternalDataModel(methods to communicate with database)
# created and implemented by Wendy, 6th Oct 2017

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, update, and_
from Authenticatemodel import User
from server import engine, Base

class Course(Base):
    __tablename__ = 'COURSE'
    id = Column(Integer, primary_key=True)
    courseCode = Column(String, nullable=False) 
    courseTime = Column(String, nullable=False)
    
    def __repr__(self):
        return "'%s' '%s'"%(self.courseCode, self.courseTime)

class Enrollment(Base):
    __tablename__ = 'ENROLLMENT'
    id = Column(Integer, primary_key=True)
    zID = Column(String, ForeignKey("USER.zID"),nullable=False) 
    courseCode = Column(String, nullable=False) 
    courseTime = Column(String, nullable=False)

    def __repr__(self):
        return "'%s' '%s' '%s'"%(self.zID, self.courseCode, self.courseTime)

class Question(Base):
    __tablename__ = 'QUESTION'
    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False) # the question
    question_type = Column(String, nullable=False) # mandatory or optional(M or O)
    question_basis = Column(String, nullable=False) # multi-choice-based(MCQ) or text-based(TB)
    
    def __repr__(self):
        return "[Question: '%s', Type = '%s', Basis = '%s']" %(self.question_text, self.question_type, self.question_basis)

class Survey(Base):
    __tablename__ = 'SURVEY'
    id = Column(Integer, primary_key=True)
    surveyName = Column(String, nullable=False) # survey name
    status = Column(String, nullable=False) # active, toBeReviewed, closed
    ExpiryDate = Column(String)

    def __repr__(self):
        return "[Survey: '%s', Status = '%s', ExpiryDate = '%s']" %(self.surveyName, self.status, self.ExpiryDate)

class QuestionInSurvey(Base):
    __tablename__ = 'QUESTIONINSURVEY'
    id = Column(Integer, primary_key=True, nullable=False)
    surveyName = Column(String, ForeignKey("SURVEY.surveyName"), nullable=False) # survey name
    questionInsurvey = Column(String, ForeignKey("QUESTION.question_text"), nullable=False) # question
    survey = relationship(Survey)
    question = relationship(Question)

    def __repr__(self):
        return "[Survey: '%s', Question = '%s']" %(self.surveyName, self.questionInsurvey)
    
class Response(Base):
    __tablename__ = 'RESPONSE'
    id = Column(Integer, primary_key=True)
    surveyName = Column(String, ForeignKey("SURVEY.surveyName"), nullable=False) # survey name
    questionInsurvey = Column(String, ForeignKey("QUESTION.question_text"), nullable=False) # question
    survey = relationship(Survey)
    question = relationship(Question)
    answer = Column(String, nullable=False)
    
    def __repr__(self):
        return "[Survey: '%s', Question = '%s', Answer = '%s']" %(self.surveyName, self.questionInsurvey, self.answer)

class FillInSurvey(Base):
    __tablename__ = 'FILLINSURVEY'
    id = Column(Integer, primary_key=True)
    surveyName = Column(String, ForeignKey("SURVEY.surveyName"), nullable=False) # survey name
    zID = Column(String, nullable=False) # zID
    survey = relationship(Survey)
    

    def __repr__(self):
        return "'%s' '%s'"%(self.surveyName, self.zID)

class InternalDataModel(object):
    
    def create_table(self):
        Base.metadata.create_all(engine)

    def search_courseOffering(self,id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        course = session.query(Course).filter(Course.id == id).first()
        session.close()
        return course.courseCode+' '+courseTime

    def get_all_courseOffering(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        courseOfferings = []
        for course in session.query(Course).all():
            courseOfferings.append(course)
        session.close()
        return courseOfferings
        # return a list of course objects, but can be printed

    def search_user_enrollments(self,zID):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        enrollments = []
        for enrollment in session.query(Enrollment).filter(Enrollment.zID == zID).all():
            enrollments.append(enrollment)
        session.close()
        return enrollments
        #return a list of enrollment objects


    def add_question(self, question_text, question_type, question_basis):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(Question(question_text=question_text, question_type=question_type, question_basis=question_basis))
        session.commit()
        session.close()

    def delete_question(self, id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(Question).filter(Question.id == id).delete()
        session.commit()
        session.close()

    def create_survey(self, surveyName, ExpiryDate):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(Survey(surveyName = surveyName, status = 'Modified', ExpiryDate = ExpiryDate))
        session.commit()
        session.close()

    def update_survey_status(self, surveyName, status):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(Survey).filter(Survey.surveyName == surveyName).update({'status': status})
        session.commit()
        session.close()

    # not used in iteration2
    def update_survey_expiryDate(self, surveyName, date):
        pass

    def add_question_to_survey(self, surveyName, question_text):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(QuestionInSurvey(surveyName=surveyName, questionInsurvey=question_text))
        session.commit()
        session.close()

    def add_fillInsurvey(self, surveyName, zID):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(FillInSurvey(surveyName=surveyName, zID=zID))
        session.commit()
        session.close()

    def add_response_to_question_in_survey(self, surveyName, question_text, answer):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(Response(surveyName=surveyName, questionInsurvey=question_text, answer = answer))
        session.commit()
        session.close()


    def delete_question_from_survey(self, surveyName, id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        question = session.query(Question).filter(Question.id == id).first()
        questions_text = quesiton.question_text
        session.query(QuestionInSurvey).filter(and_(QuestionInSurvey.surveyName == surveyName, QuestionInSurvey.questionInsurvey == question_text)).delete()
        session.commit()
        session.close()

    def get_questions(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # question here is an object, having the text, type and basis attributes
        questions = []
        for question in session.query(Question).all():
            questions.append(question)
        session.close()
        # return a list of question objects
        return questions

    def get_optional_questions(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # question here is an object, having the text, type and basis attributes
        questions = []
        for question in session.query(Question).filter(Question.question_type == 'Optional').all():
            questions.append(question)
        session.close()
        # return a list of question objects
        return questions
    
    def get_all_surveys(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # survey here is an object, similarly
        surveys = []
        for survey in session.query(Survey).all():
            surveys.append(survey)
        session.close()
        # return a list of survey objects
        return surveys

    def get_Active_surveys(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # survey here is an object, similarly
        surveys = []
        for survey in session.query(Survey).filter(Survey.status == 'Active').all():
            surveys.append(survey)
        session.close()
        # return a list of survey objects
        return surveys
     
    def get_ToBeReviewed_surveys(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        surveys = []
        for survey in session.query(Survey).filter(Survey.status == 'ToBeReviewed').all():
            surveys.append(survey)
        session.close()
        return surveys

    def get_Closed_surveys(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        surveys = []
        for survey in session.query(Survey).filter(Survey.status == 'Closed').all():
            surveys.append(survey)
        session.close()
        return surveys

    def get_specific_surveys(surveyName):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        survey = session.query(Survey).filter(Survey.surveyName == surveyName).first()
        session.close()
        return survey

    def get_questions_in_survey(self, surveyName):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        questions_text = [] # a list of question_text, not objects
        questions = [] # a list of question objects
        for row in session.query(QuestionInSurvey).filter(QuestionInSurvey.surveyName == surveyName).all():
            questions_text.append(row.questionInsurvey)
        for row in questions_text:
            questions.append(session.query(Question).filter(Question.question_text == questions_text).first())
        session.close()
        return questions

    def get_fillInsurvey_for_user(self, zID):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        fillInsurvey = session.query(FillInSurvey).filter(FillInSurvey.zID == zID).first()
        session.close()
        return fillInsurvey

    def get_all_response_for_a_question_in_survey(self, surveyName, question_text):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        answers = []
        for answerRow in session.query(Response).filter(and_(Response.surveyName == surveyName, Response.questionInsurvey == question_text)).all():
            answers.append(answerRow.answer)
        session.close()
        return answers
        # return a list of answers to a specific question in a specific survey
        # e.g. [a,a,a,b,c,b,d] all for quesiton "You like this course" in survey "COMP153 17S2" 

    def generate_results_for_survey(self, surveyName, question_text):
        pass

# Code below is for testing
# Model = IntenalDataModel()
# Model.create_table()
# Model.add_question("You like this course","Mandatory","Multi-choice")
# Model.add_question("You attend every lecture","Mandatory","Multi-choice")
# Model.add_question("What do you want to say","Optional","Text")
# for question in Model.get_questions():
#     print (question)
# Model.create_survey("COMP1531 17S2")
# for survey in Model.get_all_surveys():
#     print (survey)
# Model.add_question_to_survey("COMP1531 17S2","You like this course")
# Model.add_question_to_survey("COMP1531 17S2","You attend every lecture")
# Model.add_question_to_survey("COMP1531 17S2","What do you want to say")
# print(Model.get_questions_in_survey("COMP1531 17S2"))
# Model.delete_question_from_survey("COMP1531 17S2", "You attend every lecture")
# for question in Model.get_questions_in_survey("COMP1531 17S2"):
#     print (question)
# Model.delete_question("You attend every lecture")
# for question in Model.get_questions():
#     print (question)
# Model.update_survey_status("COMP1531 17S2", "Active")





