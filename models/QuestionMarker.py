from database.DatabaseManager import DatabaseManager

from models.Question import Question,QuestionDatabase
from models.User import User
from time import perf_counter
import random


class QuestionMarker:
     def __init__(self, Question: Question, UserAccount: User, code_to_test: str) -> None:
          self.Question = Question
          self.UserAccount = UserAccount
          self.code_to_test = code_to_test

          self.average_runtime = 0
          self.user_function = None
          self.testcases = []
          self.testcase_results = {
               "Passed":[],
               "Failed":[]
          }
          self.run_time_times = []

          self.fetch_testcases()
     
     def fetch_testcases(self):
          "Fetch the test cases for the current question."
          self.testcases = QuestionDatabase().fetch_testcases(self.Question.ID)

     #Objective 5.1 Compile code
     def compile_function(self):
          "Compile the string into a user function and return to the user if an error occurs"

          try:
               #Execute the function - in the global namespace 
               exec(self.code_to_test, globals())
               #retrieve object function from global namespace under "question_solution"
               self.user_function = globals().get('question_solution')
          except Exception as e:
               raise QuestionMarkingError(e)

          #Can't find our function - user set it under the wrong name 
          if self.user_function is None:
               raise FunctionNotFound("No function 'question_solution' found")
     
     #Objective 5.6.1 generate average runti,e
     def check_average_run_time(self):
          "Test the average runtime of the function"
          
          #Check if we have already compiled the code if not compile it
          if not self.user_function:
               self.compile_function()

          #Run the code 500 times with random test cases and store the timings.
          for i in range (0,500):
               #Select a test case.
               tcase = random.choice(self.testcases)["Input"].strip('"')

               #Run the function#
               start_time = perf_counter()

               self.user_function(tcase)

               self.run_time_times.append(perf_counter() - start_time)

          #Workout average
          self.average_runtime = sum(self.run_time_times) / len(self.run_time_times)
          return self.average_runtime
          

     #Objective 5.5.2 show failed testcases#
     def test_code_vs_testcases(self):
          "Test the user's code against the expected outputs."
          
          #Check if we have already compiled the code if not compile it
          if not self.user_function:
               self.compile_function()
          
          #RunCode and test vs testcases - make testcase list iterable
          for x, tcase in enumerate(self.testcases, 1):
               #Sets the input value and removes the surrounding quotations
               input_value = tcase["Input"].strip('"')
               output_value = tcase["Output"].strip('"')
               
               #Run the function and store the actual output
               try:
                    actual_output = self.user_function(input_value)
               except Exception as e:
                    raise RunningCodeError(e)

               #Output was correct
               if actual_output == output_value:
                    self.testcase_results["Passed"].append({input_value:actual_output})
               else:
                    self.testcase_results["Failed"].append({input_value:actual_output})
          
          return self.testcase_results

     

class QuestionMarkingError(Exception):
    """Base class for user-related exceptions."""
    def __init__(self, message="A user-related error occurred."):
        self.message = message
        super().__init__(self.message)

class CompilationError(QuestionMarkingError):
    """Exception raised when the data provided is invalid."""

    def __init__(self, details=""):
        if details:
            self.message = f"Invalid data: {details}."
        else:
            self.message = "Invalid data provided."
        super().__init__(self.message)

class FunctionNotFound(QuestionMarkingError):
    """Exception raised when the data provided is invalid."""

    def __init__(self, details=""):
        if details:
            self.message = f"Invalid data: {details}."
        else:
            self.message = "Invalid data provided."
        super().__init__(self.message)


class RunningCodeError(QuestionMarkingError):
    """Exception raised when the data provided is invalid."""

    def __init__(self, details=""):
        if details:
            self.message = f"Invalid data: {details}."
        else:
            self.message = "Invalid data provided."
        super().__init__(self.message)

          
          
