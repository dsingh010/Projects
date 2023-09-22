import os
import json
from cryptography.fernet import Fernet
from getpass import getpass

'''
This code provides a basic framework for a password manager that can add and
retrieve passwords for different websites. It uses the Fernet symmetric
encryption scheme from the cryptography library for data encryption.

Please note that this is a simplified example, and a production-ready
password manager would require much more sophisticated security features and testing.

'''

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.fernet = None
        self.data = {}

    def create_encryption_key(self):
        # Generate a strong encryption key
        return Fernet.generate_key()

    def load_data(self):
        # Load encrypted data from a file and decrypt it
        try:
            with open("passwords.json", "rb") as file:
                encrypted_data = file.read()
                self.fernet = Fernet(self.create_encryption_key())
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self.data = json.loads(decrypted_data.decode())
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def save_data(self):
        # Encrypt and save data to a file
        encrypted_data = self.fernet.encrypt(json.dumps(self.data).encode())
        with open("passwords.json", "wb") as file:
            file.write(encrypted_data)

    def add_password(self, website, username, password):
        # Add a new password entry
        self.data[website] = {"username": username, "password": password}
        self.save_data()

    def get_password(self, website):
        # Retrieve a password for a given website
        return self.data.get(website, None)

    def list_websites(self):
        # List all stored website names
        return list(self.data.keys())

def main():
    master_password = getpass("Enter your master password: ")
    password_manager = PasswordManager(master_password)
    password_manager.load_data()

    while True:
        print("\nOptions:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. List stored websites")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            password_manager.add_password(website, username, password)
        elif choice == "2":
            website = input("Enter website to retrieve password: ")
            password_entry = password_manager.get_password(website)
            if password_entry:
                print(f"Username: {password_entry['username']}")
                print(f"Password: {password_entry['password']}")
            else:
                print("Website not found.")
        elif choice == "3":
            websites = password_manager.list_websites()
            print("Stored websites:")
            for website in websites:
                print(website)
        elif choice == "4":
            password_manager.save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

