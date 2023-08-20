import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import User,UserDatabase
from models.Question import Question,QuestionDatabase
from models.QuestionAttempt import QuestionAttempt,QuestionAttemptDatabase
from datetime import datetime
from models.QuestionMarker import QuestionMarker,FunctionNotFound,QuestionMarkingError,RunningCodeError,CompilationError

class QuestionPageFrame(tk.Frame):
     def __init__(self, parent, controller, user_account : User, Question : Question):
          super().__init__(parent)
          self.controller = controller
          self.user_account = user_account
          self.Question = Question

          self.QuestionAttempt = QuestionAttemptDatabase().find_question_attempt(self.user_account.username,self.Question.ID)

          #Home Page Frame
          self.home_frame = Frame(self, bg='#ffffff', width=1920, height=1080)
          self.home_frame.pack(fill="both", expand=True)

          #Welcome Message
          self.welcome_label = Label(
               self.home_frame,
               text=f"{Question.ID} : {Question.Name}!",
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
               command=lambda: self.change_page_and_save_code_users("HomePageFrame"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.home_button.config(width=15, height=2)
          self.home_button.place(relx=0.075, y=30, anchor=CENTER)

          #Random Question Button
          self.login_button = Button(
               self.home_frame,
               text="Random Question",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
              command=lambda : self.controller.random_question(self.user_account.username),
               highlightbackground=self.home_frame['bg'] 
          )
          self.login_button.config(width=15, height=2)
          self.login_button.place(relx=0.21, y=30, anchor=CENTER)

          #SignOut button -> Back to login frame
          self.signout_button = Button(
               self.home_frame,
               text="Sign Out",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.change_page_and_save_code("LoginPageFrame"),
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
               command=lambda: self.change_page_and_save_code_users(f"UserProfileFrame"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.profile_butter.config(width=20, height=2)
          self.profile_butter.place(relx=0.9, y=30, anchor=CENTER)

          #Question Description
          self.QuestionDescription = tk.Label(self.home_frame, text=f"Question Description - {Question.Difficulty}", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.QuestionDescription.config(width=70,height=6)
          self.QuestionDescription.place(relx=0.225, y=140, anchor=CENTER)

          #Fetch question examples and format
          QuestionExamples = QuestionDatabase().fetch_question_examples(Question.ID)
          QuestionDescription = Question.Description + "\n\n" + QuestionExamples

          #Question Description box
          self.QuestionDescription = tk.Label(
          self.home_frame,
          text=QuestionDescription,
          bg="grey",
          fg="white",
          font=("Helvetica", 22, "bold"),
          wraplength=450
          )
          self.QuestionDescription.config(width=48, height=23, anchor='nw', justify='left')
          self.QuestionDescription.place(relx=0.225, y=500,anchor=CENTER)  # Adjusted anchor and coordinates

          #CodeInput
          self.code_input_label = tk.Label(self.home_frame, text="Coding Space ", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
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

          #CodeInput
          self.code_entry = tk.Text(
               self.home_frame,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white",
               wrap="word"
          )
          #Objective 4.2.2 replace attempted code into the box
          try:
               #Place either the users last attempt or the default stuff
               if self.QuestionAttempt.AttemptedCode:
                    self.code_entry.insert("1.0",self.QuestionAttempt.AttemptedCode)
          except AttributeError:
                    self.code_entry.insert("1.0",
                                        """def question_solution(variable):
               #CodeHere and return your value 
               return None"""
                                        )

          self.code_entry.bind("<FocusOut>", self.user_unfocus_the_code__box)
          self.code_entry.place(
               relx=0.72,
               rely=0.5,
               anchor=CENTER,
               width=750,
               height=450
          )


          #####Hints####
          #If those hints add the access buttons
          #Place hints in boxes (objective 4.4.1)
          if "Hint1" in self.Question.Hints:
               #Hint1Button
               self.hint1Button = Button(
                    self.home_frame,
                    text="Hint : 1",
                    relief=FLAT,
                    highlightthickness=0,
                    bg="grey",
                    font=("yu gothic ui", 15, "bold"),
                    command=lambda: self.display_hint(1),
                    highlightbackground="grey"
               )
               self.hint1Button.config(width=53, height=2)
               self.hint1Button.place(relx=0.225, y=665, anchor=CENTER)

          if "Hint2" in self.Question.Hints:
               #Hint2Button
               self.hint2Button = Button(
                    self.home_frame,
                    text="Hint : 2",
                    relief=FLAT,
                    highlightthickness=0,
                    bg="grey",
                    font=("yu gothic ui", 15, "bold"),
                    command=lambda: self.display_hint(2),
                    highlightbackground="grey"
               )
               self.hint2Button.config(width=53, height=2)
               self.hint2Button.place(relx=0.225, y=710, anchor=CENTER)

          if "Hint3" in self.Question.Hints:
               #Hint3Button
               self.hint3Button = Button(
                    self.home_frame,
                    text="Hint : 3",
                    relief=FLAT,
                    highlightthickness=0,
                    bg="grey",
                    font=("yu gothic ui", 15, "bold"),
                    command=lambda: self.display_hint(3),
                    highlightbackground="grey"
               )
               self.hint3Button.config(width=53, height=2)
               self.hint3Button.place(relx=0.225, y=755, anchor=CENTER)

          ##Submit Button####
          self.SubmitButton = Button(
               self.home_frame,
               text="Submit Code ",
               relief=FLAT,
               highlightthickness=0,
               bg="grey",
               font=("yu gothic ui", 15, "bold"),
               command = self.attempt_question_submit,
               highlightbackground="grey"
          )
          self.SubmitButton.config(width=71, height=4)
          self.SubmitButton.place(relx=0.72, y=770, anchor=CENTER)

     #Display a hint for the current question.
     def display_hint(self,hint_id: int):
          """Take the hint id in and return the question hint"""
          messagebox.showinfo("Hint",self.Question.Hints[f"Hint{hint_id}"])
     
     def user_unfocus_the_code__box(self, event):
          """Save the current code when the editor loses focus."""

          #Save the code in the db
          self.save_current_code_in_box()

     #Objective 4.2.1
     def save_current_code_in_box(self):
          """Check if any code is in the box and update the attempted date if so"""
          current_code = self.code_entry.get("1.0","end-1c")

          #Not null and added something to the solution
          if len(current_code) > 0:
               if current_code not in """def question_solution(variable):
               #CodeHere and return your value 
               return None""":
                    QuestionAttemptDatabase().update_question_attempt(self.user_account.username,self.Question.ID,current_code,datetime.now(),False)

     def change_page_and_save_code_users(self,NewPageName: str):
          """First update the attemted code then switch to the new page - acts as a passthrough to new user pages"""
          self.save_current_code_in_box()

          if NewPageName == "HomePageFrame":
               self.controller.load_home_page(self.user_account)
          else:
               self.controller.show_user_frame(NewPageName)

     #Objective (4.2.1)
     def change_page_and_save_code(self,NewPageName: str):
          """First update the attemted code then switch to the new page - acts as a passthrough to new pages"""
          self.save_current_code_in_box()

          self.controller.show_frame(NewPageName)


     def attempt_question_submit(self):
          #Get the code from the first spot to the end of the box
          current_code = self.code_entry.get("1.0","end-1c")

          #Check something is in the box
          if not current_code:
               return messagebox.showerror("Error","No valid code to submit")


          qMarker = QuestionMarker(self.Question,self.user_account,current_code)
          try:
               test_case_results = qMarker.test_code_vs_testcases()
          except FunctionNotFound:
               test_case_results = None
               return messagebox.showerror("Error","Make sure your solution is called 'question_solution'")
          except CompilationError as e:
               return messagebox.showerror("Error",f"Error : compiling your code : {e}")
          except RunningCodeError as e:
               return messagebox.showerror("Error",f"Error : running your code : {e}")
          
          #Other errors
          except Exception as e:
               return messagebox.showerror("Error",f"{e}")

          
          if not test_case_results:
               return
          
          #Check Runtime 
          qMarker.check_average_run_time()

          #Submit info to solution page -> creates solution page
          self.controller.load_solution_page(
               self.user_account,
               self.Question,
               test_case_results,
               current_code,
               qMarker.average_runtime
          )
          
          
          

               



    
	
