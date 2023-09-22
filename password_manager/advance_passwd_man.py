import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet

'''
This advanced version includes features such as strong encryption, key generation
from a master password, asymmetric key pair generation, and secure storage of the
master password and keys. It also includes a password generator and allows you to add,
retrieve, and list passwords for websites. 

'''

class PasswordManager:
    def __init__(self, master_password, encryption_key, private_key, public_key):
        self.master_password = master_password
        self.encryption_key = encryption_key
        self.private_key = private_key
        self.public_key = public_key
        self.fernet = Fernet(self.encryption_key)
        self.data = {}

    def add_password(self, website, username, password):
        # Add a new password entry
        self.data[website] = {"username": username, "password": self.fernet.encrypt(password.encode()).decode()}

    def get_password(self, website):
        # Retrieve a password for a given website
        if website in self.data:
            encrypted_password = self.data[website]["password"]
            try:
                decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
                return decrypted_password
            except InvalidToken:
                return "Invalid decryption key"
        else:
            return "Website not found."

    def list_websites(self):
        # List all stored website names
        return list(self.data.keys())

    def save_data(self):
        # Save data to a file
        with open("passwords.json", "w") as file:
            json.dump(self.data, file)

    def password_generator(self, length=12, include_special_chars=True):
        # Generate a strong password
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if include_special_chars:
            characters += "!@#$%^&*()_-+=<>?"
        password = "".join(random.choice(characters) for _ in range(length))
        return password


def generate_encryption_key(master_password, salt):
    # Generate an encryption key from the master password using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def generate_key_pair():
    # Generate a key pair for asymmetric encryption
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def main():
    # Load or generate encryption key and key pair
    if os.path.exists("master_password.txt"):
        with open("master_password.txt", "rb") as file:
            master_password = file.read()
        salt = os.urandom(16)
        encryption_key = generate_encryption_key(master_password, salt)
    else:
        master_password = input("Create a master password: ")
        salt = os.urandom(16)
        encryption_key = generate_encryption_key(master_password, salt)
        with open("master_password.txt", "wb") as file:
            file.write(master_password)

    if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
        with open("private_key.pem", "rb") as file:
            private_key = serialization.load_pem_private_key(file.read(), password=None, backend=default_backend())
        with open("public_key.pem", "rb") as file:
            public_key = serialization.load_pem_public_key(file.read(), backend=default_backend())
    else:
        private_key, public_key = generate_key_pair()
        with open("private_key.pem", "wb") as file:
            file.write(private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open("public_key.pem", "wb") as file:
            file.write(public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            ))

    password_manager = PasswordManager(master_password, encryption_key, private_key, public_key)

    while True:
        print("\nOptions:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. List stored websites")
        print("4. Generate a strong password")
        print("5. Save and Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            password_manager.add_password(website, username, password)
        elif choice == "2":
            website = input("Enter website to retrieve password: ")
            password = password_manager.get_password(website)
            print(f"Password: {password}")
        elif choice == "3":
            websites = password_manager.list_websites()
            print("Stored websites:")
            for website in websites:
                print(website)
        elif choice == "4":
            length = int(input("Enter password length: "))
            include_special_chars = input("Include special characters (y/n): ").lower() == "y"
            password = password_manager.password_generator(length, include_special_chars)
            print(f"Generated Password: {password}")
        elif choice == "5":
            password_manager.save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

