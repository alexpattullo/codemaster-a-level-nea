import bcrypt

class PasswordFunctions:
     """Useful methods for dealing with password hashes, static method means the method is called directly no need to instantianate a class"""

     @staticmethod
     def hash_pswd_bcrypt(password):
          """
          Hash a users password input to store using bcrypy algorithm
          """

          # Create a salt
          salt = bcrypt.gensalt()

          # Hash password combining the salt
          hashed_pswd = bcrypt.hashpw(password.encode(), salt)

          # Return both the hashed password and the salt
          return hashed_pswd, salt

     @staticmethod
     def check_password_hash(password, hashed_password, salt):
          # Check its encoded
          if isinstance(password, str):
               password = password.encode()

          if isinstance(hashed_password, str):
               hashed_password = hashed_password.encode()

          if isinstance(salt, str):
               salt = salt.encode()

          # Recreate the hashed password with the retrieved salt
          hashed_pswd = bcrypt.hashpw(password, salt)

          # Check the entered password against the stored hash.
          return hashed_pswd == hashed_password
