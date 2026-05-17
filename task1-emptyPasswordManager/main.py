import json
import re
import string
import secrets

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Password strength checker function (optional)
def is_strong_password(password):
    #at least 8 characters, contains uppercase, lowercase, digits, and special characters
    #use re module to check for the presence of each type of character
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


# Password generator function (optional)
def generate_password(length=16):
    """
    Generate a random strong password of the specified length.

    Args:
        length (int): The desired length of the password.

    Returns:
        str: A random strong password.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # we use the secrets module for a cryptographycally secure password
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []

# Function to add a new password
def add_password():
    """
    Add a new password to the password manager.

    This function should prompt the user for the website, username,  and password and store them to lits with same index. Optionally, it should check password strengh with the function is_strong_password. It may also include an option for the user to
    generate a random strong password by calling the generate_password function.

    Returns:
        None
    """
    website = input("Enter website name : ").strip().lower()
    username = input("Enter username : ").strip()
    succeful_input = False
    while not succeful_input :
        choice = input("Choose : \n1-Enter Password\t 2-Generate random Password\n Your choice : ")
        if choice == '1' :
            password = input("Enter Password ")
            while not is_strong_password(password):
                password = input("Password is Weak !\nPlease enter a stronger password : ")
            succeful_input = True
        elif choice == '2' :
            #for simplicity we generate a password of length 16, but you can ask the user for the desired length
            password = generate_password()
            succeful_input = True
        else :
            print("Invalid Choice !")

    encrypted_password = caesar_encrypt(password, 16)
    encrypted_passwords.append(encrypted_password)
    websites.append(website)
    usernames.append(username)

# Function to retrieve a password
def get_password():
    """
    Retrieve a password for a given website.

    This function should prompt the user for the website name and
    then display the username and decrypted password for that website.

    Returns:
        None
    """
    website = input("Enter website name : ").strip().lower()
    try:
        index = websites.index(website)
        username = usernames[index]
        encrypted_password = encrypted_passwords[index]
        password = caesar_decrypt(encrypted_password, 16)
        print(f"Username: {username}\nPassword: {password}")
    except ValueError:
        print("Website not found in the vault.")


# Function to save passwords to a JSON file
def save_passwords():
    """
    Save the password vault to a file.

    This function should save passwords, websites, and usernames to a text
    file named "vault.txt" in a structured format.

    Returns:
        None
    """

    if len(websites) != len(usernames) or len(websites) != len(encrypted_passwords) or len(usernames) != len(encrypted_passwords):
        print("Error: The lengths of websites, usernames, and encrypted_passwords lists do not match.")
        return None
    elif len(websites) == 0 :
        print("No passwords to save.")
        return None

    records = []
    for website, username, encrypted_password in zip(websites, usernames, encrypted_passwords):
        records.append(
            {
                "website": website,
                "username": username,
                "encrypted_password": encrypted_password,
            }
        )

    with open("vault.txt", "w") as file:
        json.dump(records, file, indent=4)

    print("Passwords saved successfully to vault.txt")
    return None


# Function to load passwords from a JSON file
def load_passwords():
    """
    Load passwords from a file into the password vault.

    This function should load passwords, websites, and usernames from a text
    file named "vault.txt" (or a more generic name) and populate the respective lists.

    Returns:

    """
    websites.clear()
    usernames.clear()
    encrypted_passwords.clear()

    try:
        with open("vault.txt", "r") as file:
            try:
                records = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding vault file.")
                return None
    except FileNotFoundError:
        print("Vault file not found.")
        return None

    for record in records:
        website = record.get("website")
        username = record.get("username")
        encrypted_password = record.get("encrypted_password")

        if website is None or username is None or encrypted_password is None:
            continue
        websites.append(website)
        usernames.append(username)
        encrypted_passwords.append(encrypted_password)

    return records


# Main method
def main():
# implement user interface

  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_password()
    elif choice == "2":
        get_password()
    elif choice == "3":
        save_passwords()
    elif choice == "4":
        passwords = load_passwords()
        if passwords:
            print("Passwords loaded successfully!")
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

# Execute the main function when the program is run
if __name__ == "__main__":
    main()