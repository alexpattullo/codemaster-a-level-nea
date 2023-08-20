import tkinter as tk
from tkinter import *
from tkinter import messagebox
from models.PasswordManager import PasswordFunctions
from models.User import UserDatabase,EmailAlreadyExists,UsernameAlreadyExists


class SignUpPageFrame(tk.Frame):
     def __init__(self, parent, controller):
          super().__init__(parent)
          self.controller = controller

          #Create the signup frame
          self.sgn_frame = Frame(self, bg='#ffffff', width=950, height=600)
          self.sgn_frame.pack(fill="both", expand=True)

          #Page Heading
          self.heading = Label(
               self.sgn_frame,
               text="Sign Up",
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

          #Password Label
          self.password_label = Label(
               self.sgn_frame,
               text="Password :",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.password_label.place(relx=0.275, y=195, anchor=CENTER)

          #Password Entry
          self.password_entry = Entry(
               self.sgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.password_entry.insert(0, self.controller.config_data["LoginPage"]["PasswordStandardText"])
          self.password_entry.bind("<FocusIn>", self.password_placeholder_in)
          self.password_entry.bind("<FocusOut>", self.password_placeholder_out)
          self.password_entry.place(relx=0.5, y=200, anchor=CENTER, width=270)

          #Line underneath password box
          self.password_line = Canvas(self.sgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.password_line.place(relx=0.5, y=220, anchor=CENTER)

          #Email Label
          self.email_label = Label(
               self.sgn_frame,
               text="Email (Optional) :",
               bg="white",
               fg="black",
               font=("yu gothic ui", 25, "bold")
          )
          self.email_label.place(relx=0.245, y=245, anchor=CENTER)

          #Email Entry
          self.email_entry = Entry(
               self.sgn_frame,
               highlightthickness=0,
               relief=FLAT,
               bg="#D3D3D3",
               fg="grey",
               font=("yu gothic ui", 15, "bold"),
               insertbackground="white"
          )
          self.email_entry.insert(0, self.controller.config_data["LoginPage"]["EmailStandardText"])
          self.email_entry.bind("<FocusIn>", self.email_placeholder_in)
          self.email_entry.bind("<FocusOut>", self.email_placeholder_out)
          self.email_entry.place(relx=0.5, y=250, anchor=CENTER, width=270)

          # Line underneath email box
          self.email_line = Canvas(self.sgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
          self.email_line.place(relx=0.5, y=270, anchor=CENTER)

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
          
          #Signup Button
          self.sign_up_button = Button(
               self.sgn_frame,
               text="SIGN UP",
               relief=FLAT,
               highlightthickness=0,
               bg=self.sgn_frame['bg'],
               font=("yu gothic ui", 15, "bold"),
               highlightbackground=self.sgn_frame['bg'],
               command=self.signup_attempt
          )
          self.sign_up_button.place(relx=0.405, y=300, anchor=CENTER)

     #Objective 1.3 (User can create an account using unique password and username)
     def signup_attempt(self):
          #Fetch inputs from panel
          username = self.username_entry.get()
          password = self.password_entry.get()
          #Objective 1.4 (Users password is hashed )
          hashed_new_password,custom_salt = PasswordFunctions.hash_pswd_bcrypt(password)
          email = self.email_entry.get()

          #Verify there is some input
          if not username or not password or username == self.controller.config_data["LoginPage"]["UsernameStandardText"] or password == self.controller.config_data["LoginPage"]["PasswordStandardText"]:
               return messagebox.showerror("Login Failed", "ERROR : Invalid username or password")
          
          #Verify password
          #Objective 1.6 and 1.6.1(Check password requirements)
          valid_password,pswd_info = self.controller.verify_password_requirements(password)
          if not valid_password:
               return messagebox.showerror("Invalid Password", pswd_info)
          
          #Verify email
          #User hasn't attempted to set an email

          #Objective 1.3.1 (optional email field)
          if email == self.controller.config_data["LoginPage"]["EmailStandardText"]:
               email = None

          if email:
               #
               valid_email = self.controller.verify_email_address(email)
               if not valid_email:
                    return messagebox.showerror("Login Failed", "ERROR : Invalid email address")
          
          #Create User
          #Objective 1.3 (Create the user account)
          try:
               UserDatabase().create_user(username,hashed_new_password,email,custom_salt)

          #Username not unique
          except UsernameAlreadyExists:
               return messagebox.showerror("Signup Failed", "ERROR : Username already exists in the database")
          
          #Email not unique
          except EmailAlreadyExists:
               return messagebox.showerror("Signup Failed", "ERROR : Email already exists in the database")

          #Redirected back to login page
          messagebox.showinfo("Signup Success","Your account has been created")
          self.controller.show_frame("LoginPageFrame")





     def username_placeholder_in(self, event):
          "Method to delete the placeholder in username box"
          if self.username_entry.get() == self.controller.config_data["LoginPage"]["UsernameStandardText"]:
               self.username_entry.delete(0, "end")

     def username_placeholder_out(self, event):
          "Method to replace the placeholder in username box"
          if not self.username_entry.get():
               self.username_entry.insert(0, self.controller.config_data["LoginPage"]["UsernameStandardText"])


     def email_placeholder_in(self, event):
          "Method to delete the placeholder in email box"
          if self.email_entry.get() == self.controller.config_data["LoginPage"]["EmailStandardText"]:
               self.email_entry.delete(0, "end")

     def email_placeholder_out(self, event):
          "Method to replace the placeholder in email box"
          if not self.email_entry.get():
               self.email_entry.insert(0, self.controller.config_data["LoginPage"]["EmailStandardText"])


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
