class surveys:
    def __init__(self,survey_name,mandatory_list=[], optional_list=[]):
        self._survey_name = survey_name
        self._mandatory_list = mandatory_list
        self._optional_list = optional_list

    def add_mandatory_question(self, new_Mquestion):
        self._mandatory_list.append(new_Mquestion)
    def delete_mandatory_question(self, Mquestion_index):
        del self.mandatory_list[Mquestion_index]

    def add_optional_question(self, new_Oquestion):
        self._optional_list.append(new_Oquestion)
    def delete_optional_question(self, Oquestion_index):
        del self.optional_list[Oquestion_index]

    def get_survey_name(self):
        return self._survey_name
    def get_mandatory_list(self):
        return self._mandatory_list
    def get_optional_list(self):
        return self._optional_list

