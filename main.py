from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    # Generate a key & store it in a file
    def create_key(self, path):     
      
        self.key = Fernet.generate_key() 
        # print(self.key)

        # store key into a file
        with open(path, 'wb') as f:
            f.write(self.key)

    
    # Load file w/ key -> for decoding encrypted info/files
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
       self.password_file = path

       if initial_values is not None:
           for key, value in initial_values.items(): 
               self.add_password(key, value)

    def load_password_file(self, path):  
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(" : ")
                # site, encrypted = line.split(" - ")

                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

        
    def add_password(self, website, password):
        self.password_dict[website] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(website + " : " + encrypted.decode() + "\n\n")
                # f.write(website + " - " + encrypted.decode() + "\n")

    
    def get_password(self, website):
        return self.password_dict[website]

    
def main():
    password = {
        "email": "adrian123",
        "facebook": "facebookpassword",
        "youtube": "helloworld",
        "twitter": "mynameisthepassword"
    }

    pm = PasswordManager()

    print("""What would you like to do?

    1. Create new key
    2. Load existing key
    3. Create new password file
    4. Load existing password file
    5. Add new password
    6. Get a password
    Q. Quit
    """)

    done = False
    while not done:
        choice = input("Enter your choice: ")

        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice == "5":
            website = input("Enter the website: ")
            password = input("Enter password:")
            pm.add_password(website, password)
        elif choice == "6":
            website = input("Which website do you want: ")
            print(f"Password for {website} is {pm.get_password(website)}")
        elif choice == "Q":
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
