import sqlite3
import datetime as dt
from datetime import datetime,timezone
from database.DatabaseManager import DatabaseManager
from models.Question import Question
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import ast

class User:
     def __init__(
               self,
               user_data
          ):

          self.username = user_data[0]
          self.password = user_data[1]
          self.email = user_data[2]
          self.PasswordSalt = user_data[3]
          self.registration_date = user_data[4]
     
     def generate_userinfo_piechart(self, question_info: dict):
          """Generate a piechart displaying the remaining questions for a user to attempt"""

          if all(stats['attempted'] == 0 for key, stats in question_info.items() if key != 'Total'):
               question_info["EASY"]['attempted']= 1

          # Calculate percentages
          attempted_counts = {}
          unattempted_counts = {}

          # Fix the qinfo dictionary to be processable
          del question_info["Total"]
          for difficulty in question_info:
               if question_info[difficulty]['total'] == 0:
                    question_info[difficulty]['total'] = 1
          
          #Go through each question difficulty and count the attempted number of questions
          for difficulty, stats in question_info.items():
               attempted_counts[difficulty] = stats['attempted']

               # Ensure unattempted count is non-negative
               unattempted_counts[difficulty] = stats['total'] - stats['attempted'] if stats['total'] > 0 else 0

          # Plotting
          labels = ['Attempted', 'Unattempted']
          attempted_sizes = [sum(attempted_counts.values()), sum(unattempted_counts.values())]

          #Determine colours for type of question
          colors_attempted = ['green', 'orange', 'red']
          #Colours for unattemped questions
          colors_unattempted = ['lightgreen', 'lightsalmon', 'lightcoral']

          #Figure size and position inside frame
          fig = Figure(figsize=(2.4, 2.4), facecolor="grey")
          ax = fig.add_subplot(111)

          # Check if attempted_sizes contains any NaN values
          if any(math.isnan(size) for size in attempted_sizes):
               print("Invalid sizes for pie chart. Skipping pie chart generation.")
               return None

          #Attempted vs Unattempted plot
          ax.pie(attempted_sizes, autopct='%1.0f%%', startangle=90, colors=['lightblue', 'lightgrey'])

          # Draw inner pies (Each type of question attemt)
          ax.pie(attempted_counts.values(), radius=0.8, colors=colors_attempted, labeldistance=0.7, startangle=90)
          ax.pie(unattempted_counts.values(), radius=0.8, colors=colors_unattempted, labeldistance=0.7, startangle=90)

          #Aspect ratios
          ax.set(aspect="equal",)
          return fig


          

 



class UserDatabase(DatabaseManager):
     def __init__(self):
          super().__init__()
          self.initialise_database()

     def find_user_by_username(self,username:str):
          "Method to find a user by username, return None if not found"

          #Query db via username
          self.db_cursor.execute("SELECT * FROM UserAccount WHERE Username=?", (username,))
          user_data = self.db_cursor.fetchone()

          #Return user object if found else None
          if user_data:
               return User(user_data)

          return None
     
     def delete_question_attempts_by_username(self, username: str):
          """Find and delete all question attempts associated with the username"""

          #Delete where matches
          self.db_cursor.execute("DELETE FROM QuestionAttempts WHERE Username=?", (username,))

          self.db_connection.commit()


     def find_user_question_stats(self,username: str) -> dict:
          "Method to create the question stats for the home page on a specific user"
          q_info = {
               "EASY":{
                   "attempted":0,
                   "total":0
               },
               "MEDIUM":{
                   "attempted":0,
                   "total":0
               },
               "HARD":{
                   "attempted":0,
                   "total":0
               }
          }

          #Find Attempted Questions 
          self.db_cursor.execute('''
          SELECT Difficulty
          FROM Question q 
          JOIN QuestionAttempts qa ON q.QuestionID = qa.QuestionID 
          WHERE qa.Username = ?
          ''', (username,))
          attemps = self.db_cursor.fetchall()

          #Number of question attempts for each difficulty
          for attempt in attemps:
              dificulty = attempt[0]
              q_info[dificulty]["attempted"] += 1
          
          #Number of questions total for each difficulty
          self.db_cursor.execute(f'''
          SELECT Difficulty, COUNT(*) FROM Question GROUP BY Difficulty
          ''')
          difficulty_counts = self.db_cursor.fetchall()

          for difficulty, count in difficulty_counts:
               q_info[difficulty]["total"] = count
          

          # Calculate the total number of questions attempted
          total_attempted = sum(q_info[difficulty]["attempted"] for difficulty in q_info)
          try:
               q_info["Total"] = f"{round(total_attempted / sum(q_info[difficulty]['total'] for difficulty in q_info) * 100)}%"     
          except ValueError:
              q_info["Total"] = 0
          
          return q_info

     def fetch_user_unattempted_questions(self, username: str):
          """Method to fetch all unattempted questions for a given username"""

          #Fetch unattempted q
          self.db_cursor.execute("""
               SELECT q.*
               FROM Question q
               LEFT JOIN QuestionAttempts qa ON q.QuestionID = qa.QuestionID AND qa.Username = ?
               WHERE qa.Username IS NULL
          """, (username,))

          rows = self.db_cursor.fetchall()

          # Process the fetched questions
          return [Question(row) for row in rows]

     def get_user_ranking(self, username: str):
          """Fetch a user's ranking based on their question attempts"""
          #Query returing all the users and their question attempts
          self.db_cursor.execute("""
               SELECT Username, COUNT(*) AS Attempts
               FROM QuestionAttempts
               GROUP BY Username
               ORDER BY Attempts DESC
          """)

          user_rank = 0
          user_attempts = 0

          # Iterate over each user's attempts and set ranking of our user
          for index, row in enumerate(self.db_cursor.fetchall(), start=1):
               if row[0] == username:
                    user_rank = index
                    user_attempts = row[1]
                    break

          return user_rank, user_attempts

     def get_top_attempts(self, period='today'):
          "Fetch the top user attempts based on a certain timeframe"
          current_date = datetime.now()
          if period == 'today':
               start_date = datetime.combine(dt.date.today(),dt.time.min) 
          elif period == 'this_month':
               start_date = dt.date(current_date.year, current_date.month, 1)
          else:
               raise ValueError("Invalid period param passed, use 'today' or 'this_month'")

          #Filter db by completion time
          self.db_cursor.execute("""
               SELECT Username, COUNT(*) AS Attempts
               FROM QuestionAttempts
               WHERE CompletionTime >= ? AND CompletionTime <= ?
               GROUP BY Username
               ORDER BY Attempts DESC
               LIMIT 1
          """, (start_date, current_date))

          top_username = self.db_cursor.fetchone()
          return top_username[0] if top_username else None

     def create_user(self, username: str, password: str, email: str, PasswordSalt):
          "Method to create a user object in the UserAccount Table"
          user_already = self.find_user_by_username(username)
          if user_already:
               raise UsernameAlreadyExists(username)

          registration_date = datetime.now(timezone.utc)
          if email == "example@email.com...":
               email = None

          try:
               #Insert values and save
               self.db_cursor.execute('''INSERT INTO UserAccount (Username, Password, EmailAddress,PswdSalt, RegistrationDate)
                                   VALUES (?, ?, ?, ?, ?)''', (username, password.decode(), email,PasswordSalt.decode(), registration_date))
               self.db_connection.commit()
          except sqlite3.IntegrityError as e:
               #Raise the relevant error.

               if "UserAccount.Username" in e:
                    raise UsernameAlreadyExists(username)
               if "UserAccount.EmailAddress" in e:
                    raise EmailAlreadyExists(email)

          except Exception as e:
               print(e)

     def update_user(self, username: str, column_name: str, new_value: str ):
          "Method to update user informatuon in the UserAccount Table"

          self.db_cursor.execute(
               f'''
               UPDATE UserAccount
               SET {column_name} = "{new_value}"
               WHERE Username = "{username}"
               '''
               )
          self.db_connection.commit()

class UserError(Exception):
    """Base class for user-related exceptions."""
    def __init__(self, message="A user-related error occurred."):
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExists(UserError):
    """Execption raised when the user already exists in the database"""

    def __init__(self, username):
        self.message = f"User '{username}' already exists in the database"
        super().__init__(self.message)

class UserNotFound(UserError):
    """Execption raised when the user already exists in the database"""

    def __init__(self, username):
        self.message = f"User '{username}' already exists in the database"
        super().__init__(self.message)


class EmailAlreadyExists(UserError):
    """Execption raised when the user already exists in the database"""

    def __init__(self, emailaddress):
        self.message = f"Email '{emailaddress}' already exists in the database"
        super().__init__(self.message)


class InvalidDataError(UserError):
    """Exception raised when the data provided is invalid."""

    def __init__(self, details=""):
        if details:
            self.message = f"Invalid data: {details}."
        else:
            self.message = "Invalid data provided."
        super().__init__(self.message)
