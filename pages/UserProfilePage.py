import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import User,UserDatabase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.PasswordManager import PasswordFunctions

class UserProfileFrame(tk.Frame):
     def __init__(self, parent, controller, user_account : User):
          super().__init__(parent)
          self.controller = controller
          self.user_account = user_account

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

          ###########Userinformation#################

          #Edit Userinformation
          self.title_label = tk.Label(self.home_frame, text="Edit User information", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=82,height=6)
          self.title_label.place(relx=0.4875, y=140, anchor=CENTER)

          #Backdrop - top left
          self.title_label = tk.Label(self.home_frame, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=40,height=14)
          self.title_label.place(relx=0.355, y=353, anchor=CENTER)

          #Backdrop - bottom left
          self.title_label = tk.Label(self.home_frame, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=40,height=15)
          self.title_label.place(relx=0.355, y=637, anchor=CENTER)

          #Backdrop - top right
          self.title_label = tk.Label(self.home_frame, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=40,height=14)
          self.title_label.place(relx=0.61, y=353, anchor=CENTER)

          #Backdrop - bottom right
          self.title_label = tk.Label(self.home_frame, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.title_label.config(width=40,height=15)
          self.title_label.place(relx=0.61, y=637, anchor=CENTER)

          #Change Username
          self.total_rank = tk.Label(self.home_frame, text=f"New Username :", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_rank.config(width=19,height=6)
          self.total_rank.place(relx=0.355, y=353, anchor=CENTER)

          self.username_entry = Entry(
               self.home_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.username_entry.place(relx=0.355, y=383, anchor=CENTER, width=200)

          #Change Password
          self.total_rank = tk.Label(self.home_frame, text=f"New Password :", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_rank.config(width=19,height=6)
          self.total_rank.place(relx=0.355, y=637, anchor=CENTER)

          self.password_entry = Entry(
               self.home_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.password_entry.place(relx=0.355, y=667, anchor=CENTER, width=200)

          #Change EmailAddress
          self.total_rank = tk.Label(self.home_frame, text=f"New Email :", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_rank.config(width=19,height=6)
          self.total_rank.place(relx=0.61, y=353, anchor=CENTER)

          self.email_entry = Entry(
               self.home_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.email_entry.place(relx=0.61, y=383, anchor=CENTER, width=200)


          #Reset Question Stats
          self.total_rank = tk.Label(self.home_frame, text=f"Reset Question\nStats", font=("Helvetica", 24, "bold"), bg="#B2BEB5", fg="white")
          self.total_rank.config(width=19,height=6)
          self.total_rank.place(relx=0.61, y=637, anchor=CENTER)

          self.rQuestionStats = Button(
               self.home_frame,
               text="Reset Stats",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'] ,
               font=("yu gothic ui", 15, "bold"),
               command= self.reset_question_stats,
               highlightbackground=self.home_frame['bg'] 
          )
          self.rQuestionStats.config(width=15, height=2)
          self.rQuestionStats.place(relx=0.61, y=687, anchor=CENTER)


          #Apply Changes Button
          self.ApplyChangesB = Button(
               self.home_frame,
               text="ApplyChanges",
               relief=FLAT,
               highlightthickness=0,
               bg=self.home_frame['bg'] ,
               font=("yu gothic ui", 15, "bold"),
               command= self.apply_update_changes,
               highlightbackground=self.home_frame['bg'] 
          )
          self.ApplyChangesB.config(width=17, height=3)
          self.ApplyChangesB.place(relx=0.85, y=815, anchor=CENTER)



          #########RankingInfo###########

          #Ranking Title
          self.ranking_label = tk.Label(self.home_frame, text="Total Ranking", font=("Helvetica", 16, "bold"), bg="grey", fg="white")
          self.ranking_label.config(width=35,height=6)
          self.ranking_label.place(relx=0.85, y=140, anchor=CENTER)

          #Ranking Title Backdrop
          self.ranking_label_backdrop = tk.Label(self.home_frame,bg="grey", fg="white")
          self.ranking_label_backdrop.config(width=35,height=35)
          self.ranking_label_backdrop.place(relx=0.85, y=500, anchor=CENTER)


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


     def apply_update_changes(self):
          """Take all the input boxes determine if anything has changed and update in the database"""
          new_username = self.username_entry.get()
          new_password = self.password_entry.get()
          hashed_new_password,custom_salt = PasswordFunctions.hash_pswd_bcrypt(new_password)
          new_email = self.email_entry.get()

          user_db = UserDatabase()

          #Update Username
          #Objective (2.1.1)
          if new_username:
               if self.user_account.username == new_username:
                    return messagebox.showerror("Error","New username cannot be equal to the old username")

               #Update Username in the database
               user_db.update_user(self.user_account.username,"Username",new_username)
               messagebox.showinfo("Success","I have successfully updated your username")


          #Update Password
          #Objective (2.1.3)
          if new_password:
               
               if self.user_account.password == new_password:
                    return messagebox.showerror("Error","New password cannot be equal to the old password")
               
               
               #Verify meets requirements
               #Objective 2.2.2
               valid_password,pswd_info = self.controller.verify_password_requirements(new_password)
               if not valid_password:
                    return messagebox.showerror("Invalid Password", pswd_info)

               #Update Password in the database
               user_db.update_user(self.user_account.username,"Password",hashed_new_password.decode())
               user_db.update_user(self.user_account.username,"PswdSalt",custom_salt.decode())
               messagebox.showinfo("Success","I have successfully updated your password")


          #Update Email
          #Objective (2.1.2)
          if new_email:
               if self.user_account.email == new_email:
                    return messagebox.showerror("Error","New email cannot be equal to the old email")
               
               #Verify meets requirements
               #Objective 2.2.1
               valid_email = self.controller.verify_email_address(new_email)
               if not valid_email:
                    return messagebox.showerror("Error", "ERROR : Invalid email address")
               
               #Update Email in the database
               user_db.update_user(self.user_account.username,"EmailAddress",new_email)
               messagebox.showinfo("Success","I have successfully updated your email address")

          user_db.close_connection()

     #Objective 2.3 (Users can reset their stats with a button)
     def reset_question_stats(self):
          #Delete all question attempts belonging to the user.
          UserDatabase().delete_question_attempts_by_username(self.user_account.username)

          #Tell user
          messagebox.showinfo("Success", "Deleted all relevant question attempts")
