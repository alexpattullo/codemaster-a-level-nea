import sqlite3
import json
from pathlib import Path

class DatabaseManager:
     def __init__(self):
          self.db_connection = None
          self.db_cursor = None
          # Resolve paths from this file so the app can be launched from any
          # working directory (for example, with `python main.py`).
          project_root = Path(__file__).resolve().parent.parent
          self._db_path = project_root / "database" / "CodeMaster.db"
          self._question_info_path = project_root / "preloadeddata" / "questions.json"

     def initialise_database(self):
          if not self._db_path.exists():
               print("database file does not exist. Creating a new one...")
          
          self.db_connection = sqlite3.connect(self._db_path)
          self.db_cursor = self.db_connection.cursor()
          

     def close_connection(self):
          self.db_connection.close()

     def create_tables(self):
          # User Account table
          self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS UserAccount(
                                   Username VARCHAR(255) UNIQUE,
                                   Password VARCHAR(255),
                                   EmailAddress VARCHAR(255),
                                   PswdSalt VARCHAR(255),
                                   RegistrationDate DATE NOT NULL,
                                   PRIMARY KEY (Username)
                              )''')

          # Question table
          self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Question(
                                   QuestionID INT UNIQUE,
                                   QuestionName TEXT NOT NULL,
                                   QuestionDescription TEXT NOT NULL,
                                   Hints JSON,
                                   Difficulty VARCHAR(255) NOT NULL,
                                   TypeOfQuestion JSON NOT NULL,
                                   PRIMARY KEY (QuestionID)
                              )''')

          # Question Attempts table
          self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS QuestionAttempts(
                                   Username VARCHAR(255),
                                   QuestionID INT,
                                   AttemptedCode TEXT,
                                   CompletionTime DATE NOT NULL,
                                   Passed BOOLEAN DEFAULT false,
                                   FOREIGN KEY (Username) REFERENCES UserAccount(Username),
                                   FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID),
                                   PRIMARY KEY (Username, QuestionID)
                              )''')

          # Test Cases table
          self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS TestCases(
                                   TestCaseID INT UNIQUE,
                                   QuestionID INT,
                                   Input TEXT NOT NULL,
                                   Output TEXT NOT NULL,
                                   FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID),
                                   PRIMARY KEY (TestCaseID)
                              )''')

          self.db_connection.commit()
          
          #Load the question data.
          self.load_questions_from_json()

     def load_questions_from_json(self):
          """Load the questions from the data file into SQLite."""

          #Open the question data file.
          with self._question_info_path.open('r', encoding='utf-8') as file:
               questions_data = json.load(file)

          #Delete all current questions
          self.db_cursor.execute('''
               DELETE FROM Question;
          ''')
          self.db_cursor.execute('''
               DELETE FROM TestCases;
          ''')
          self.db_connection.commit()

          #Load each question into the database.
          for question in questions_data:
               self.insert_question(question)

     def insert_question(self, question):
          """Load the question into the database"""
          question_data = (
               question["QuestionID"],
               question["QuestionName"],
               question["QuestionDescription"],
               json.dumps(question["Hints"]),
               question["Difficulty"],
               json.dumps(question["TypeOfQuestion"])
          )
          #Add our questions 
          self.db_cursor.execute('''
               INSERT INTO Question (QuestionID, QuestionName, QuestionDescription, Hints, Difficulty, TypeOfQuestion)
               VALUES (?, ?, ?, ?, ?, ?)
          ''', question_data)

          #Load the examples into the test-case table.
          for example in question["Examples"]:
               self.insert_example(question["QuestionID"], example)

          self.db_connection.commit()

     def insert_example(self, question_id, example):
          """Insert a test case into the database."""

          #Use the next available test-case number.
          self.db_cursor.execute("SELECT COUNT(*) FROM TestCases")
          current_count = self.db_cursor.fetchone()[0]
          testcase_id = current_count + 1

          #Data passed from the question data file.
          example_data = (
               testcase_id,
               question_id,
               json.dumps(example["Input"]),  # Convert JSON object to string
               example["Output"]
          )

          #Insert testcase into table
          self.db_cursor.execute('''
               INSERT INTO TestCases (TestCaseID, QuestionID, Input, Output)
               VALUES (?, ?, ?, ?)
          ''', example_data)

          self.db_connection.commit()
