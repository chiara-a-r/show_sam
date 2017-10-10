# This may be merged with the other models files later, only for login module for now #
# By Wendy on 30 Sep #

from flask_login import UserMixin
import sqlite3

class User(UserMixin):
    def __init__(self, id, password, role):
        self.id = id
        self.password = password
        self.role = role

class authenticateModel(object):
    def search_detail(self, zID):
        query = "SELECT password, role from USER where zID = '%s' " % zID
        user_detail = self.dbselect(query)
        return user_detail
    def dbselect(self, query):
        connection = sqlite3.connect('survey.db')
        cursorObj = connection.cursor()
        rows = cursorObj.execute(query)
        connection.commit()
        results = []
        for row in rows:
            results.append(row)
        cursorObj.close()
        return results
