import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import User,UserDatabase
from models.Question import Question,QuestionDatabase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HomePageFrame(tk.Frame):
     def __init__(self, parent, controller, user_account : User):
          super().__init__(parent)
          self.controller = controller
          self.user_account = user_account

          #Type of filter 
          self.question_filter = 0

          #Home Page Frame
          self.home_frame = Frame(self, bg='#ffffff', width=1920, height=1080)
          self.home_frame.pack(fill="both", expand=True)

          #Welcome Message
          self.welcome_label = Label(
               self.home_frame,
               text=f"Welcome, {user_account.username}!",
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

          #Lessons page button
          self.lessons_button = Button(
               self.home_frame,
               text="Lessons",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=self.controller.lessons_attempt,
               highlightbackground=self.home_frame['bg'] 
          )
          self.lessons_button.config(width=15, height=2)
          self.lessons_button.place(relx=0.345, y=30, anchor=CENTER)

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
               command=lambda: self.controller.show_user_frame(f"UserProfileFrame"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.profile_butter.config(width=20, height=2)
          self.profile_butter.place(relx=0.9, y=30, anchor=CENTER)
          
          #Progress counter Title
          self.title_label = tk.Label(self.home_frame, text="Progress Counter", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=35,height=6)
          self.title_label.place(relx=0.125, y=140, anchor=CENTER)

          #Progress counter info backdrop
          self.title_label_backdrop = tk.Label(self.home_frame,bg="grey", fg="white")
          self.title_label_backdrop.config(width=35,height=35)
          self.title_label_backdrop.place(relx=0.125, y=500, anchor=CENTER)
          
          user_db = UserDatabase()
          user_information = user_db.find_user_question_stats(self.user_account.username)

          #Total - progress counter
          self.total_pc = tk.Label(self.home_frame, text=f"Total : {user_information['Total']}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_pc.config(width=19,height=2)
          self.total_pc.place(relx=0.125, y=500, anchor=CENTER)

          #EASY - progress counter
          self.total_pc = tk.Label(self.home_frame, text=f"Easy : {user_information['EASY']['attempted']}/{user_information['EASY']['total']}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="green")
          self.total_pc.config(width=19,height=2)
          self.total_pc.place(relx=0.125, y=575, anchor=CENTER)


          #Medium - progress counter
          self.total_pc = tk.Label(self.home_frame, text=f"Medium : {user_information['MEDIUM']['attempted']}/{user_information['MEDIUM']['total']}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="orange")
          self.total_pc.config(width=19,height=2)
          self.total_pc.place(relx=0.125, y=650, anchor=CENTER)

          #Hard - progress counter
          self.total_pc = tk.Label(self.home_frame, text=f"Hard : {user_information['HARD']['attempted']}/{user_information['HARD']['total']}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="red")
          self.total_pc.config(width=19,height=2)
          self.total_pc.place(relx=0.125, y=725, anchor=CENTER)

          #PieChart 
          #Display the user's progress chart.
          fig = self.user_account.generate_userinfo_piechart(user_information)

          #Add to Canvas
          canvas = FigureCanvasTkAgg(fig, master=self.home_frame)
          canvas.draw()

          # Add the canvas to the Tkinter window
          canvas.get_tk_widget().place(relx=0.125, y=350, anchor=CENTER)

          #PieChart Title
          self.pc_title = tk.Label(self.home_frame, text=f"Attempted vs Unattempted", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.pc_title.config(width=22,height=1)
          self.pc_title.place(relx=0.125, y=250, anchor=CENTER)

          ###########ProgrammingQuestions#################

          #Programming Questions Title
          self.title_label = tk.Label(self.home_frame, text="Programing Questions", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=60,height=6)
          self.title_label.place(relx=0.42, y=140, anchor=CENTER)

          #Filter Completed Button
          self.filter_completed = Button(
               self.home_frame,
               text="By Completed",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.filter_question_scrollbar("by_completed"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.filter_completed.config(width=16, height=3)
          self.filter_completed.place(relx=0.6725, y=110, anchor=CENTER)

          #Filter Difficulty Button
          self.filter_completed = Button(
               self.home_frame,
               text="By Difficulty",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.filter_question_scrollbar("by_difficulty"),
               highlightbackground=self.home_frame['bg'] 
          )
          self.filter_completed.config(width=16, height=3)
          self.filter_completed.place(relx=0.6725, y=172, anchor=CENTER)

          #ScrollBar
          #Display all available questions in a scrollable list.
          all_questions = QuestionDatabase().fetch_all_questions()
          self.generate_scrollbar(all_questions)






          #########RankingInfo###########

          #Ranking Title
          self.ranking_label = tk.Label(self.home_frame, text="Total Ranking", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.ranking_label.config(width=35,height=6)
          self.ranking_label.place(relx=0.85, y=140, anchor=CENTER)

          #Ranking Title Backdrop
          self.ranking_label_backdrop = tk.Label(self.home_frame,bg="grey", fg="white")
          self.ranking_label_backdrop.config(width=35,height=35)
          self.ranking_label_backdrop.place(relx=0.85, y=500, anchor=CENTER)

          #Display the number of completed questions.

          #Userinfo
          user_rank, user_attempts = user_db.get_user_ranking(self.user_account.username)
          top_today = user_db.get_top_attempts("today")
          top_this_month = user_db.get_top_attempts("this_month")

          #Total - ranking
          self.total_rank = tk.Label(self.home_frame, text=f"Total Ranking:\n{user_rank}th place", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_rank.config(width=19,height=6)
          self.total_rank.place(relx=0.85, y=315, anchor=CENTER)

          #Total - today
          self.today_rank = tk.Label(self.home_frame, text=f"Top Today:\n{top_today}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.today_rank.config(width=19,height=6)
          self.today_rank.place(relx=0.85, y=500, anchor=CENTER)

          #Total - month
          self.month_rank = tk.Label(self.home_frame, text=f"Top This Month:\n{top_this_month}", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.month_rank.config(width=19,height=6)
          self.month_rank.place(relx=0.85, y=685, anchor=CENTER)

          #Close the database connection
          user_db.close_connection()




     #Create the scrollable question list.
     def generate_scrollbar(self,all_questions: list[Question]):
          #Create a frame to hold the scrollbar
          frame = Frame(
               self.home_frame,
          #     width=1200,
            #   height=1200
          )
          frame.place(relx=0.485, y=500, anchor=CENTER)

          #Creat the scrollbar
          scrollbar1 = Scrollbar(
               frame,
               orient=VERTICAL
          )
          scrollbar1.pack(side=RIGHT, fill=Y)

          #Create the canvas
          canvas1 = Canvas(
               frame,
               yscrollcommand=scrollbar1.set,
               width=700,
               height=550
          )
          canvas1.pack(side=LEFT, fill=BOTH, expand=True)

          #Configure waht happens when the scrollbar is "Scrolled"
          scrollbar1.config(command=canvas1.yview)

          myframe1 = Frame(canvas1)
          canvas1.create_window((0, 0), window=myframe1, anchor="nw")

          #Add our questions 
          for question in all_questions:
               button = Button(
                    myframe1,
                    text=f"{question.ID} : {question.Name} - {question.Difficulty}",
                    height=5,
                    width=72,
                    command=lambda q=question: self.controller.load_question_page(self.user_account,q)
               )
               button.pack()

          #Update apperance immediately rather than waiting for event loop
          myframe1.update_idletasks()
          canvas1.config(scrollregion=canvas1.bbox("all"))


     #Option to filter scrollbar Objectives (3.4.1,3.4.2)
     def filter_question_scrollbar(self,filter_param):
          """Filter question scrollbar by completed/difficulty"""
          if filter_param == "by_completed":
               #Fetch list of unattempted questions
               unattempted_questions = UserDatabase().fetch_user_unattempted_questions(self.user_account.username)
               self.generate_scrollbar(unattempted_questions)

          #Click once to adds to filter number -> each time clicked skip to next filter
          if filter_param == "by_difficulty":
               q_db = QuestionDatabase()
               if self.question_filter == 0:
                    #Find Questions from filter
                    questions = q_db.fetch_questions_by_difficulty("EASY")
                    self.generate_scrollbar(questions)

                    #Next filter option
                    self.question_filter += 1
                    return
               
               if self.question_filter == 1:
                    #Find Questions from filter
                    questions = q_db.fetch_questions_by_difficulty("MEDIUM")
                    self.generate_scrollbar(questions)

                    #Next filter option
                    self.question_filter += 1
                    return

               if self.question_filter == 2:
                    #Find Questions from filter
                    questions = q_db.fetch_questions_by_difficulty("HARD")
                    self.generate_scrollbar(questions)

                    #Next filter option
                    #Reset counter to 0
                    self.question_filter = 0
                    return
