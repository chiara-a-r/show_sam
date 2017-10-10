# this is the model to communicate with ENROLLENT and COURSEOFFERING TABLE
import sqlite3

class ExternalDataModel(object):
    
    def get_all_courseOffering(self):
        query = "SELECT courseCode, courseTime from COURSES " 
        courseOfferings = self.dbselect(query)
        return CourseOfferings # it is a list of tuples, e.g. [(COMP1531,17S2),(COMP2521,17S2)]
    
    def search_user_enrollments(self,zID):
        query = "SELECT courseCode, courseTime from ENROLLMENT where zID = '%s' " %zID
        enrollments = self.dbselect(query)
        return enrollments # it is a list of tuples, e.g. [(COMP1531,17S2),(COMP2521,17S2)]

    def dbselect(self, query):
        connection = sqlite3.connect('sqlite:///SurveySystem.db')
        cursorObj = connection.cursor()
        rows = cursorObj.execute(query)
        connection.commit()
        results = []
        for row in rows:
            results.append(row)
        cursorObj.close()
        return results