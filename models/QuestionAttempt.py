from database.DatabaseManager import DatabaseManager
from datetime import datetime


class QuestionAttempt:
     def __init__(
               self,
               user_data
          ):

          self.Username = user_data[0]
          self.QuestionID = user_data[1]
          self.AttemptedCode = user_data[2]
          self.CompletionTime = user_data[3]
          self.Passed = user_data[4]
          
class QuestionAttemptDatabase(DatabaseManager):
     def __init__(self):
          super().__init__()
          self.initialise_database()

     def update_question_attempt(self, username: str, question_id: int, attempted_code: str, completion_time: datetime,passed=False):
          """Find and update a question attempt / make a new one if it doesn't exist"""

          #Get the attempt for the supplied username and question ID.
          self.db_cursor.execute("SELECT * FROM QuestionAttempts WHERE Username=? AND QuestionID=?", (username, question_id))
          existing_attempt = self.db_cursor.fetchone()

          #Update existing attempt
          if existing_attempt:
               if existing_attempt[4] == True and not passed:
                    passed = True
               self.db_cursor.execute("""
               UPDATE QuestionAttempts
               SET AttemptedCode=?, CompletionTime=?, Passed=?
               WHERE Username=? AND QuestionID=?
               """, (attempted_code, completion_time,passed, username, question_id))
          #Insert a new attempt
          else:
               self.db_cursor.execute("""
               INSERT INTO QuestionAttempts (Username, QuestionID, AttemptedCode, CompletionTime, Passed)
               VALUES (?, ?, ?, ?, ?)
               """, (username, question_id, attempted_code, completion_time,passed))
               
          self.db_connection.commit()

     def find_question_attempt(self, username: str, question_id: int):
          """Find a question attempt and return object"""

          self.db_cursor.execute("SELECT * FROM QuestionAttempts WHERE Username=? AND QuestionID=?", (username, question_id))
          existing_attempt = self.db_cursor.fetchone()

          #Make QuestionAttemptObject
          if existing_attempt:
               return QuestionAttempt(existing_attempt)
          return None



class QuestionAttemptError(Exception):
    """Base class for user-related exceptions."""
    def __init__(self, message="A user-related error occurred."):
        self.message = message
        super().__init__(self.message)
