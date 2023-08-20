import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import UserDatabase
from models.PasswordManager import PasswordFunctions

class ForgotPasswordFrame(tk.Frame):
     def __init__(self, parent, controller):
          super().__init__(parent)
          self.controller = controller

          #Create the signup frame
          self.sgn_frame = Frame(self, bg='#ffffff', width=950, height=600)
          self.sgn_frame.pack(fill="both", expand=True)

          #Page Heading
          self.heading = Label(
               self.sgn_frame,
               text="Reset Password",
               font=('yu gothic ui', 55, "bold"),
               bg="white",
               fg='black',
               bd=5,
               relief=FLAT
          )
          self.heading.place(relx=0.5, y=30, anchor=CENTER)

          #Username Label
          self.username_label = Label(
               self.sgn_frame,
               text="Username :",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.username_label.place(relx=0.275, y=145, anchor=CENTER)

          #Username Entry
          self.username_entry = Entry(
               self.sgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.username_entry.insert(0, self.controller.config_data["LoginPage"]["UsernameStandardText"])
          self.username_entry.bind("<FocusIn>", self.username_placeholder_in)
          self.username_entry.bind("<FocusOut>", self.username_placeholder_out)
          self.username_entry.place(relx=0.5, y=150, anchor=CENTER, width=270)



          #Line below username box
          self.username_line = Canvas(self.sgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.username_line.place(relx=0.5, y=170, anchor=CENTER)

          #OldPassword Label
          self.old_password_label = Label(
               self.sgn_frame,
               text="Old Password :",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.old_password_label.place(relx=0.245, y=195, anchor=CENTER)

          #OldPassword Entry
          self.old_password_entry = Entry(
               self.sgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.old_password_entry.place(relx=0.5, y=200, anchor=CENTER, width=270)

          #Background text for the password box
          self.old_password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
          self.old_password_entry.bind("<FocusIn>", self.old_password_placeholder_in)
          self.old_password_entry.bind("<FocusOut>", self.old_password_placeholder_out)
          self.old_password_entry.place(relx=0.5, y=200, anchor=CENTER, width=270)

          #Line underneath old password box
          self.old_password_line = Canvas(self.sgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.old_password_line.place(relx=0.5, y=220, anchor=CENTER)

          #NewPassword Label
          self.new_password_label = Label(
               self.sgn_frame,
               text="New Password :",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.new_password_label.place(relx=0.245, y=245, anchor=CENTER)

          #NewPassword Entry
          self.new_password_entry = Entry(
               self.sgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          #Background text for the password box
          self.new_password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
          self.new_password_entry.bind("<FocusIn>", self.new_password_placeholder_in)
          self.new_password_entry.bind("<FocusOut>", self.new_password_placeholder_out)
          self.new_password_entry.place(relx=0.5, y=250, anchor=CENTER, width=270)

          #Line underneath new password box
          self.new_password_line = Canvas(self.sgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.new_password_line.place(relx=0.5, y=270, anchor=CENTER)

          #Login Button
          self.login_button = Button(
               self.sgn_frame,
               text="BACK",
               relief=FLAT,
               highlightthickness=0,
               bg=self.sgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               highlightbackground=self.sgn_frame['bg'],
               command=lambda: self.controller.show_frame("LoginPageFrame")
          )
          self.login_button.place(relx=0.5, y=300, anchor=CENTER)
          
          #Reset Password Button
          self.reset_password_button = Button(
               self.sgn_frame,
               text="Reset Password",
               relief=FLAT,
               highlightthickness=0,
               bg=self.sgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               highlightbackground=self.sgn_frame['bg'],
               command=self.reset_password_attempt
          )
          self.reset_password_button.place(relx=0.38, y=300, anchor=CENTER)


     def username_placeholder_in(self, event):
          "Method to delete the placeholder in username box"
          if self.username_entry.get() == self.controller.config_data["LoginPage"]["UsernameStandardText"]:
               self.username_entry.delete(0, "end")

     def username_placeholder_out(self, event):
          "Method to replace the placeholder in username box"
          if not self.username_entry.get():
               self.username_entry.insert(0, self.controller.config_data["LoginPage"]["UsernameStandardText"])

     def old_password_placeholder_in(self, event):
          "Method to delete the placeholder in password box"
          if self.old_password_entry.get() == self.controller.config_data["LoginPage"]["PasswordStandardText"]:
               self.old_password_entry.delete(0, "end")
               self.old_password_entry.config(show="*", fg="black")

     def old_password_placeholder_out(self, event):
          "Method to replace the placeholder in password box"
          if not self.old_password_entry.get():
               self.old_password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
               self.old_password_entry.config(show="", fg="grey")


     def new_password_placeholder_in(self, event):
          "Method to delete the placeholder in password box"
          if self.new_password_entry.get() == self.controller.config_data["LoginPage"]["PasswordStandardText"]:
               self.new_password_entry.delete(0, "end")
               self.new_password_entry.config(show="*", fg="black")

     def new_password_placeholder_out(self, event):
          "Method to replace the placeholder in password box"
          if not self.new_password_entry.get():
               self.new_password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
               self.new_password_entry.config(show="", fg="grey")

     #Objective 1.5
     def reset_password_attempt(self):
          #Fetch page inputs
          username = self.username_entry.get()
          old_password = self.old_password_entry.get()
          new_password = self.new_password_entry.get()

          #Form hashed version of the passwords
          #Objective 1.4
          hashed_new_password,custom_salt = PasswordFunctions.hash_pswd_bcrypt(new_password)

          if not username or not old_password or not new_password:
               return messagebox.showerror("Invalid Inputs","All values are required")
          
          db_user = UserDatabase()
          
          #Check the username.
          User = db_user.find_user_by_username(username)
          if not User:
               return messagebox.showerror("Invalid Username", "ERROR : This is not a valid username assigned to an account")

          #Verify password contents
          if not PasswordFunctions.check_password_hash(old_password, User.password,User.PasswordSalt):
               return messagebox.showerror("Invalid Password", "ERROR : This is not the correct password for this account")

          #Check new password is new and not the same as the old password
          if old_password == new_password:
               return messagebox.showerror("Invalid Password", "ERROR : You cannot change the password to the same password")
          

          #Check that the new password meets the requirements.
          valid_password,extra_password_info = self.controller.verify_password_requirements(new_password)
          if not valid_password:
               return messagebox.showerror("Invalid Password", extra_password_info)
          
          #Reset Password in the database
          db_user.update_user(User.username,"Password",hashed_new_password.decode())
          db_user.update_user(User.username,"PswdSalt",custom_salt.decode())
          db_user.close_connection()

          messagebox.showinfo("Updated Password", "Sign in again with your new password")

          #Take user back to the login page to resign in
          self.controller.show_frame("LoginPageFrame")
