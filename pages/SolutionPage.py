import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import User
from models.Question import Question,QuestionDatabase
from models.QuestionAttempt import QuestionAttemptDatabase
from datetime import datetime

class SolutionPageFrame(tk.Frame):
     def __init__(self, parent, controller, user_account : User, Question: Question,Testcases: dict,UserSolution,average_runtime: float):
          super().__init__(parent)
          self.controller = controller

          self.user_account = user_account
          self.Question = Question
          self.Testcases = Testcases
          self.UserSolution = UserSolution
          self.AverageRuntime = average_runtime
          #{'Passed': [{'alex': 'xela'}, {'python': 'nohtyp'}, {'golf': 'flog'}], 'Failed': []}

          #Home Page Frame
          self.home_frame = Frame(self, bg='#ffffff', width=1920, height=1080)
          self.home_frame.pack(fill="both", expand=True)

          #Welcome Message
          self.welcome_label = Label(
               self.home_frame,
               text=f"{Question.ID} : {Question.Name}",
               font=('yu gothic ui', 30, "bold"),
               bg="white",
               fg='black',
               bd=5,
               relief=FLAT
          )
          self.welcome_label.place(relx=0.5, y=30, anchor=CENTER)

          self.password_line = Canvas(self.home_frame, width=1550, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.password_line.place(relx=0.5, y=75, anchor=CENTER)

          #Home page button
          self.home_button = Button(
               self.home_frame,
               text="Home",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.controller.load_home_page(self.user_account),
               highlightbackground=self.home_frame['bg'] 
          )
          self.home_button.config(width=15, height=2)
          self.home_button.place(relx=0.075, y=30, anchor=CENTER)

          #Objective (5.4.1) next question button
          #Next Question
          self.login_button = Button(
               self.home_frame,
               text="Next Question",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               #Move to the next question, or return to the first question.
               command=lambda: self.controller.load_question_page(self.user_account,QuestionDatabase().fetch_question_by_id(f"{self.Question.ID + 1 if self.Question.ID + 1 <= 11 else 1}")),
               highlightbackground=self.home_frame['bg'] 
          )
          self.login_button.config(width=40, height=4)
          self.login_button.place(relx=0.8275, y=770, anchor=CENTER)

          #Objective (5.4.2) random question button
          #Random Question Button
          self.login_button = Button(
               self.home_frame,
               text="Random Question",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.controller.random_question(self.user_account.username),
               highlightbackground=self.home_frame['bg'] 
          )
          self.login_button.config(width=30, height=4)
          self.login_button.place(relx=0.555, y=770, anchor=CENTER)

          #SignOut button -> Back to login frame
          self.signout_button = Button(
               self.home_frame,
               text="Sign Out",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.controller.show_frame("LoginPageFrame"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.signout_button.config(width=20, height=2)
          self.signout_button.place(relx=0.7275, y=30, anchor=CENTER)


          #Profile Page Button
          self.profile_butter = Button(
               self.home_frame,
               text="Profile",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda : self.controller.show_user_frame("UserProfileFrame"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.profile_butter.config(width=20, height=2)
          self.profile_butter.place(relx=0.9, y=30, anchor=CENTER)
          
          #Right hand side - display code

          #CodeInput
          self.code_input_label = tk.Label(self.home_frame, text="Your Solution", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.code_input_label.config(width=90,height=3)
          self.code_input_label.place(relx=0.72, y=112, anchor=CENTER)

          #CodeInputBackdrop1
          self.CodeInputBackdrop1 = tk.Label(self.home_frame,bg="grey", fg="white")
          self.CodeInputBackdrop1.config(width=90,height=35)
          self.CodeInputBackdrop1.place(relx=0.72, y=437, anchor=CENTER)
          #CodeInputBackdrop2
          self.CodeInputBackdrop2 = tk.Label(self.home_frame, font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.CodeInputBackdrop2.config(width=55,height=19)
          self.CodeInputBackdrop2.place(relx=0.72, y=437, anchor=CENTER)


          #UsersActualSolution
          self.CodeInputBackdrop3 = tk.Label(
               self.home_frame,
               text=self.UserSolution,
               font=("yu gothic ui", 15, "bold"),
               bg="#D3D3D3",
               fg="grey",
               justify="left"
              # wrap="word"
          )
          self.CodeInputBackdrop3.config(width=65,height=27)
          self.CodeInputBackdrop3.place(relx=0.72, y=437, anchor=CENTER)
          
          #Objective 5.3 (pass of fail stated at the top)
          passed = f"FAILED ({len(Testcases['Failed'])}/{len(Testcases['Failed'])+len(Testcases['Passed'])})"
          if len(Testcases["Passed"]) == 3 and len(Testcases["Failed"]) == 0:
               passed = "PASSED"

               QuestionAttemptDatabase().update_question_attempt(self.user_account.username,self.Question.ID,self.UserSolution,datetime.now(),True)
               
               #Passed so update question attempt as passed

          #TestcaseReview
          self.TestcaseDescription = tk.Label(self.home_frame, text=f"{Question.Name} - {passed}", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.TestcaseDescription.config(width=70,height=6)
          self.TestcaseDescription.place(relx=0.225, y=140, anchor=CENTER)


          #Average Runtime
          #Objective 5.6.1 average runtime
          self.RuntimeInfo = tk.Label(self.home_frame, text=f"Average Runtime\n {self.AverageRuntime}s", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.RuntimeInfo.config(width=70,height=9)
          self.RuntimeInfo.place(relx=0.225, y=300, anchor=CENTER)

          y_place = 455
          number_tcase = 1 
          
          #Objective 5.5.1, 5.5.2 testcase info
          #Go through each testcase if passed add as green box else red box
          for tcase in self.Testcases["Passed"]:
               #Add box
               self.Tcase1 = tk.Label(self.home_frame, text=f"Testcase {number_tcase}: Accepted", font=("Helvetica", 16, "bold"), bg="green", fg="white")
               self.Tcase1.config(width=70,height=6)
               self.Tcase1.place(relx=0.225, y=y_place, anchor=CENTER)  
               
               #Next item 130 down
               y_place += 130
               number_tcase += 1

          for tcase in self.Testcases["Failed"]:
               #Fetch the key value pair ie the input and failed output
               fail_info = ""
               for key, value in tcase.items():
                    fail_info = f"{key} -> {value}"

               #Add box
               self.Tcase1 = tk.Label(self.home_frame, text=f"Testcase {number_tcase}: Failed\n{fail_info}", font=("Helvetica", 16, "bold"), bg="red", fg="white")
               self.Tcase1.config(width=70,height=6)
               self.Tcase1.place(relx=0.225, y=y_place, anchor=CENTER)  
               
               #Next item 130 down
               y_place += 130
               number_tcase += 1
  

