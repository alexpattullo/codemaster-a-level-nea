from database.DatabaseManager import DatabaseManager
import json


class Question:
     def __init__(
               self,
               user_data
          ):

          self.ID = user_data[0]
          self.Name = user_data[1]
          self.Description = user_data[2]
          self.Hints = json.loads(user_data[3])
          self.Difficulty = user_data[4]
          self.TypeOfQuestion = user_data[5]
          
class QuestionDatabase(DatabaseManager):
     def __init__(self):
          super().__init__()
          self.initialise_database()

     def fetch_all_questions(self):
          "Return every question in the database."

          #Query db via username
          self.db_cursor.execute("SELECT * FROM Question")
          all_question_data = self.db_cursor.fetchall()

          return [Question(q_data) for q_data in all_question_data]


     def fetch_testcases(self, question_id):
          """Return the test cases for a question."""
          testcases = []

          #Find in db
          self.db_cursor.execute("SELECT Input, Output FROM TestCases WHERE QuestionID=?", (question_id,))
          testcase_data = self.db_cursor.fetchall()

          #Place into dict in list
          for input_val, output_val in testcase_data:
               testcases.append({"Input": input_val, "Output": output_val})
          return testcases

     def fetch_question_by_id(self,question_id):
          "Fetch a question from db and return as its question object by its id"

          self.db_cursor.execute("SELECT * FROM Question WHERE QuestionID=?", (question_id,))
          q_data = self.db_cursor.fetchone()

          return Question(q_data)
     
     def fetch_question_examples(self, question_id):
          examples_query = '''
               SELECT Input, Output
               FROM TestCases
               WHERE QuestionID = ?
          '''

          self.db_cursor.execute(examples_query, (question_id,))
          examples_data = self.db_cursor.fetchall()

          formatted_examples = []
          for idx, example_data in enumerate(examples_data, start=1):
               input_val, output_val = example_data
               formatted_example = f"- {input_val} -> {output_val}"
               formatted_examples.append(formatted_example)

          return "Examples :\n" + "\n".join(formatted_examples)


     def fetch_questions_by_difficulty(self, difficulty):
          """Method to fetch questions by difficulty"""

          #Query db
          self.db_cursor.execute("SELECT * FROM Question WHERE Difficulty=?", (difficulty,))
          question_data = self.db_cursor.fetchall()

          return [Question(q_data) for q_data in question_data]  

class QuestionError(Exception):
    """Base class for user-related exceptions."""
    def __init__(self, message="A user-related error occurred."):
        self.message = message
        super().__init__(self.message)
