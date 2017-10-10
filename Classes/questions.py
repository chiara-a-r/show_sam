class questions(object):
    def __init__(self,question,mandatory = True):
        self._question = question
        mandatory = mandatory

    def get_question(self,question):
        return self._question
    def get_type(self, mandatory):
        if mandatory:
            return "Mandatory"
        return "Optional"

class MCQ(questions):
    def __init__(self, question, mandatory, question_options):
        questions.__init__(question, mandatory)
        self._question_options = ["Strongly agree","Agree","Neither agree nor disagree","Disagree","Strongly disagree"]

    def get_question_options(self, question_options):
        return self._question_options

class TextBQ(questions):
    def __init__(self, question, mandatory):
        questions,__init__(question, mandatory)

