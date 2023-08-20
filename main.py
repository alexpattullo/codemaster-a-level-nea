import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import User,UserDatabase
import json
import random
from pathlib import Path

#DB Manager
from database.DatabaseManager import DatabaseManager
from models.Question import QuestionDatabase,Question

#Login pages
from pages.LoginPage import LoginPageFrame
from pages.SignupPage import SignUpPageFrame
from pages.ForgotPasswordPage import ForgotPasswordFrame

#Account pages
from pages.HomePage import HomePageFrame
from pages.QuestionPage import QuestionPageFrame
from pages.UserProfilePage import UserProfileFrame
from pages.SolutionPage import SolutionPageFrame

class AppManager(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            #Load configuration once so it is available to each page.
            config_path = Path(__file__).resolve().parent / "config.json"
            with config_path.open("r", encoding="utf-8") as f:
                self.config_data = json.load(f)

            #Initialize database
            self._database = DatabaseManager()
            self._database.initialise_database()
            self._database.create_tables()


            #Create container to hold each page 
            self.container = tk.Frame(self)
            self.container.pack(fill=tk.BOTH, expand=True)

            #Adaptable size both horizontal and vertical
            self.container.pack(side="top", fill="both", expand=True)
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)   
            
            #Attribute to hold pages
            self._frames = {}    
            self._user_account_frames = {}  


            #Each page added to frame with key as the class
            for F in (LoginPageFrame,SignUpPageFrame,ForgotPasswordFrame):
                frame = F(self.container, self)
                self._frames[F.__name__] = frame

                #Each page overlaps each other 
                frame.grid(row=0, column=0, sticky="nsew")
            
            #Initialise window and load up login page
            self.show_frame("LoginPageFrame")


        def show_frame(self, page_name):
            """Method used to place a new page ontop of the current one, allowing to switch screens/pages"""

            #Raise to front

            frame = self._frames[page_name]
            frame.tkraise() 
        
        def show_user_frame(self, page_name):
            """Method used to place a new page ontop of the current one, allowing to switch screens/pages"""

            #Raise to front

            frame = self._user_account_frames[page_name]
            frame.tkraise() 

        def load_question_page(self, User : User, Question: Question):
            #Custom method for solution page as it requires specific variables to be passed rather than be able to be created at the start
            frame = QuestionPageFrame(self.container,self,User,Question)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise() 

        def load_solution_page(self, User : User, Question: Question, Testcases : dict,code_solution: str,av_runtime: float):
            #Custom method for solution page as it requires specific testcase info to be passed to it 
            frame = SolutionPageFrame(self.container,self,User,Question,Testcases,code_solution,av_runtime)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise() 

        def load_home_page(self, User : User):
            #Custom method for home page as piechart needs to be refreshed each time its called
            frame = HomePageFrame(self.container,self,User)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise() 

        def initialise_login_frames(self, User: User):
            #Pre load each page with the user once they are loade d
            for F in (HomePageFrame,UserProfileFrame):
                frame = F(self.container, self, User)
                self._user_account_frames[F.__name__] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            
            #Preload each question so they can be accessed
            for Question in QuestionDatabase().fetch_all_questions():
                frame = QuestionPageFrame(self.container,self,User,Question)
                self._user_account_frames[f"QuestionPageFrame{Question.ID}"] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            
        #Choose a random question for the user.
        def random_question(self,username):
            """Select a random question and take the user to that page"""  

            #Number non attempted questions

            #Pick a random question ID.
            random_item = random.choice([Question for Question in QuestionDatabase().fetch_all_questions()])
            #Send user to said page
            self.load_question_page(UserDatabase().find_user_by_username(username),random_item) 

        #Validate password requirements and return any missing criteria.
        def verify_password_requirements(self,password:str):
            extra_password_info = ""
            try:
                password = str(password)
            except ValueError:
                extra_password_info += f"Password is not a valid string\n"

            #Check it actually exists
            if not password:
                extra_password_info += f"No valid input\n"

            #Length
            if len(password) < 5 :
                extra_password_info += f"Password is shorter than 5 characters\n"

            #No Upper case letters
            if password.lower() == password:
                extra_password_info += f"No uppercase letters found\n"

            #At least one digit.
            if not any(char.isdigit() for char in password):
                extra_password_info += f"No digits found\n"
            
            #No failed info so passed
            if len(extra_password_info) == 0:
                return True,""
            
            extra_password_info = f"Password : {password}\n" + extra_password_info
            return False,extra_password_info

        #Perform a basic email address validation.
        def verify_email_address(self,email_address: str):
            #Some email server of sort e.g .com/.co/.gov etc
            if "." not in email_address:
                return False
            
            if "@" not in email_address:
                return False
            
            split = email_address.split("@")


            #Check for valid emailname e.g alex and a valid email server e.g. icloud.com
            try:
                if len(split[0]) == 0:
                        return False
                if len(split[1]) == 0:
                        return False
            except Exception as e:
                return False     

            return True     

        def lessons_attempt(self):
            messagebox.showinfo("Coming Soon","This feature is coming shortly...")
            
class CustomError(Exception):
     """Base class for custom exceptions."""
     def __init__(self, message="A custom error occurred."):
          self.message = message
          super().__init__(self.message)


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()

