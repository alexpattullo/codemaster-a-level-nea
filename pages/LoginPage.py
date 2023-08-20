import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.User import UserDatabase
from models.PasswordManager import PasswordFunctions

class LoginPageFrame(tk.Frame):
     def __init__(self, parent, controller):
          super().__init__(parent)
          self.controller = controller

          #Create the login frame
          self.lgn_frame = Frame(self, bg='#ffffff', width=950, height=600)
          self.lgn_frame.pack(fill="both", expand=True)

          #Page Heading
          self.heading = Label(
               self.lgn_frame,
               text=self.controller.config_data["ProjectName"],
               font=('yu gothic ui', 55, "bold"),
               bg="white",
               fg='black',
               bd=5,
               relief=FLAT
          )
          self.heading.place(relx=0.5, y=30, anchor=CENTER)

          #Author Label
          self.by_label = Label(
               self.lgn_frame,
               text=f"by {self.controller.config_data['ProjectAuthor']}",
               font=('yu gothic ui', 14),
               bg="white",
               fg='black',
               bd=0,
               relief=FLAT
          )
          self.by_label.place(relx=0.5, y=63, anchor=CENTER)

          #Username Label
          self.username_label = Label(
               self.lgn_frame,
               text="Username",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.username_label.place(relx=0.5, y=150, anchor=CENTER)

          #Username Entry
          self.username_entry = Entry(
               self.lgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          #Background text for the username box
          self.username_entry.insert(0, self.controller.config_data["LoginPage"]["UsernameStandardText"])
          self.username_entry.bind("<FocusIn>", self.username_placeholder_in)
          self.username_entry.bind("<FocusOut>", self.username_placeholder_out)
          self.username_entry.place(relx=0.5, y=185, anchor=CENTER, width=270)

          #Line below username box
          self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.username_line.place(relx=0.5, y=205, anchor=CENTER)

          #Password Label
          self.password_label = Label(
               self.lgn_frame,
               text="Password",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.password_label.place(relx=0.5, y=225, anchor=CENTER)
     
          #Password Entry
          self.password_entry = Entry(
               self.lgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          #Background text for the password box
          self.password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
          self.password_entry.bind("<FocusIn>", self.password_placeholder_in)
          self.password_entry.bind("<FocusOut>", self.password_placeholder_out)
          self.password_entry.place(relx=0.5, y=260, anchor=CENTER, width=270)

          #Line underneath password box
          self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.password_line.place(relx=0.5, y=280, anchor=CENTER)

          #Show password Button - Objective 1.2 (1.2.1 Button displaying users plaintext password)
          self.show_password_button = Button(
               self.lgn_frame,
               text="Show",
               relief=FLAT,
               highlightthickness=0,
               bg=self.lgn_frame['bg'],
               highlightbackground=self.lgn_frame['bg'],
               font=("yu gothic ui", 12, "bold"),
          )
          #Bind events to methods
          self.show_password_button.bind("<ButtonPress-1>", self.show_password)
          self.show_password_button.bind("<ButtonRelease-1>", self.hide_password)
          self.show_password_button.place(relx=0.6, y=225, anchor=CENTER)

          #Login Button
          self.login_button = Button(
               self.lgn_frame,
               text="LOGIN",
               relief=FLAT,
               highlightthickness=0,
               bg=self.lgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               highlightbackground=self.lgn_frame['bg'],
               command=self.login_attempt
          )
          self.login_button.place(relx=0.5, y=300, anchor=CENTER)
          
          #Signup Button
          self.login_button = Button(
               self.lgn_frame,
               text="Create Account",
               relief=FLAT,
               highlightthickness=0,
               bg=self.lgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               highlightbackground=self.lgn_frame['bg'],
               command=lambda: self.controller.show_frame("SignUpPageFrame")
          )
          self.login_button.place(relx=0.3775, y=300, anchor=CENTER)

          #Forgot Password Button
          self.login_button = Button(
               self.lgn_frame,
               text="Forgot Password",
               relief=FLAT,
               highlightthickness=0,
               bg=self.lgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               command=lambda: self.controller.show_frame("ForgotPasswordFrame"),
               highlightbackground=self.lgn_frame['bg'] 
          )
          self.login_button.place(relx=0.625, y=300, anchor=CENTER)

     #Objective 1.1 (Users to can sign into their account using their unique usernames and passwords)
     def login_attempt(self):
          username = self.username_entry.get()
          password = self.password_entry.get()
          
          #Verify there is some input
          if not username or not password or username == self.controller.config_data["LoginPage"]["UsernameStandardText"] or password == self.controller.config_data["LoginPage"]["PasswordStandardText"]:
               return messagebox.showerror("Login Failed", "ERROR : Invalid username or password")
          
          #Fetch the user object from the database 
          user_db = UserDatabase().find_user_by_username(username)
          if not user_db:
               return messagebox.showerror("Login Failed", "ERROR : Invalid username")
          
          #Check password is correct checking hashed version
          if not PasswordFunctions.check_password_hash(password,user_db.password,user_db.PasswordSalt):
               return messagebox.showerror("Login Failed", "ERROR : Incorrect Password")
          
          #Success - Home page 
          messagebox.showinfo("Success", "Successful login")
          #Initialise all the remaining user frames
          self.controller.initialise_login_frames(user_db)
          #Take the user to the home page
          self.controller.load_home_page(user_db)
     
     #Objective 1.2
     def show_password(self, event):
          """Method to remove the *'s hiding a users password from people looking at their screen"""
          self.password_entry.config(show="")

     def hide_password(self, event):
          """Method to rehide a users password after they have toggled the button"""
          self.password_entry.config(show="*")


     def username_placeholder_in(self, event):
          "Method to delete the placeholder in username box"
          if self.username_entry.get() == self.controller.config_data["LoginPage"]["UsernameStandardText"]:
               self.username_entry.delete(0, "end")

     def username_placeholder_out(self, event):
          "Method to replace the placeholder in username box"
          if not self.username_entry.get():
               self.username_entry.insert(0, self.controller.config_data["LoginPage"]["UsernameStandardText"])

     def password_placeholder_in(self, event):
          "Method to delete the placeholder in password box"
          if self.password_entry.get() == self.controller.config_data["LoginPage"]["PasswordStandardText"]:
               self.password_entry.delete(0, "end")
               self.password_entry.config(show="*", fg="black")

     def password_placeholder_out(self, event):
          "Method to replace the placeholder in password box"
          if not self.password_entry.get():
               self.password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
               self.password_entry.config(show="", fg="grey")
