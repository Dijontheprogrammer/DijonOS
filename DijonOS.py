import time
import os
import sys
import math
import getpass
import hashlib

def startup():
    print("Starting up DijonOS...")
    time.sleep(1)
    file_exists = os.path.exists("log.txt")
    with open("log.txt", "a") as log_file:
        if file_exists:
            log_file.write("DijonOS started successfully at {}\n".format(time.ctime()))
        else:
            log_file.write("Created log.txt and started DijonOS at {}\n".format(time.ctime()))
    print("DijonOS is now running.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def logging_in():
    def create_account():
        print("=== Create a New Account ===")
        username = input("Choose a username: ")
        # Prevent duplicate usernames
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as acc_file:
                for line in acc_file:
                    if line.strip() and line.split(":", 1)[0] == username:
                        print("Username already exists. Please choose another.\n")
                        return
        password = getpass.getpass("Choose a password: ")
        hashed_password = hash_password(password)
        # Save credentials (username:hashed_password)
        with open("accounts.txt", "a") as acc_file:
            acc_file.write(f"{username}:{hashed_password}\n")
        # Create user folder
        user_folder = os.path.join(os.getcwd(), username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        print(f"Account created for {username}. You can now log in.\n")
        # Log account creation in main log file
        with open("log.txt", "a") as log_file:
            log_file.write(f"Account created for {username} at {time.ctime()}\n")

    def check_credentials(username, password):
        hashed_password = hash_password(password)
        if not os.path.exists("accounts.txt"):
            return False
        with open("accounts.txt", "r") as acc_file:
            for line in acc_file:
                if ":" not in line:
                    continue
                saved_user, saved_pass = line.strip().split(":", 1)
                if username == saved_user and hashed_password == saved_pass:
                    return True
        return False

    print("DijonOS is running.")
    print("Welcome to DijonOS!")
    logged_in = False
    while not logged_in:
        choice = input("Do you want to (l)ogin or (c)reate an account? ").lower()
        if choice == "c":
            create_account()
        elif choice == "l":
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            if check_credentials(username, password):
                print(f"Welcome, {username}!")
                user_folder = os.path.join(os.getcwd(), username)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                # Log user login in main log file
                with open("log.txt", "a") as log_file:
                    log_file.write(f"User {username} logged in at {time.ctime()}\n")
                logged_in = True
            else:
                print("Incorrect username or password. Access denied.\n")
        else:
            print("Invalid option. Please choose 'l' or 'c'.\n")
    return username  # Return the logged-in username

if __name__ == "__main__":
    startup()
    current_user = logging_in()
    print("DijonOS is now ready for use.")
    while True:
        command = input(f"{current_user}@DijonOS:~$ ")
        if command.lower() == "exit":
            print("Exiting DijonOS. Goodbye!")
            break
        elif command.lower() == "help":
            print("Available commands:")
            print("  help                Show this help message")
            print("  exit                Exit DijonOS")
            print("  shutdown            Shutdown DijonOS")
            print("  whoami              Show current user")
            print("  log                 Show the main log file")
            print("  clear               Clear the screen")
            print("  create <filename>   Create a new text file in your folder")
            print("  delete <filename>   Delete a file from your folder")
            print("  rename <old> <new>  Rename a file in your folder")
            print("  view <filename>     View a file's contents")
            print("  edit <filename>     Edit a file's contents")
            print("  search <keyword>    Search for a keyword in your files")
            print("  upload_image <filename>  Simulate uploading an image")
        elif command.lower() == "whoami":
            print(f"You are logged in as {current_user}.")
        elif command.lower() == "log":
            if os.path.exists("log.txt"):
                with open("log.txt", "r") as log_file:
                    print(log_file.read())
            else:
                print("Log file does not exist.")
        elif command.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Screen cleared.")
        elif command.lower().startswith("create"):
            # Usage: create filename.txt
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: create <filename>")
            else:
                filename = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)  # Ensure user folder exists
                file_path = os.path.join(user_folder, filename)
                if os.path.exists(file_path):
                    print(f"File '{filename}' already exists in your folder.")
                else:
                    with open(file_path, "w") as f:
                        print("Enter text for the file (end with an empty line):")
                        lines = []
                        while True:
                            content = input()
                            if content == "":
                                break
                            lines.append(content)
                        f.write("\n".join(lines))
                    print(f"File '{filename}' created in your folder.")

        if command.lower().startswith("delete"):
            # Usage: delete filename.txt
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: delete <filename>")
            else:
                filename = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                file_path = os.path.join(user_folder, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"File '{filename}' deleted from your folder.")
                else:
                    print(f"File '{filename}' does not exist in your folder.")
        elif command.lower().startswith("rename"):
            # Usage: rename old_filename.txt new_filename.txt
            parts = command.split(maxsplit=2)
            if len(parts) < 3:
                print("Usage: rename <old_filename> <new_filename>")
            else:
                old_filename = parts[1]
                new_filename = parts[2]
                user_folder = os.path.join(os.getcwd(), current_user)
                old_file_path = os.path.join(user_folder, old_filename)
                new_file_path = os.path.join(user_folder, new_filename)
                if os.path.exists(old_file_path):
                    os.rename(old_file_path, new_file_path)
                    print(f"File '{old_filename}' renamed to '{new_filename}'.")
                else:
                    print(f"File '{old_filename}' does not exist in your folder.")
        elif command.lower().startswith("view"):
            # Usage: view filename.txt
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: view <filename>")
            else:
                filename = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                file_path = os.path.join(user_folder, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        print(f.read())
                else:
                    print(f"File '{filename}' does not exist in your folder.")
        elif command.lower().startswith("edit"):
            # Usage: edit filename.txt
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: edit <filename>")
            else:
                filename = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                file_path = os.path.join(user_folder, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()
                    print("Current content of the file:")
                    print(content)
                    print("Enter new content (end with an empty line):")
                    lines = []
                    while True:
                        new_content = input()
                        if new_content == "":
                            break
                        lines.append(new_content)
                    with open(file_path, "w") as f:
                        f.write("\n".join(lines))
                    print(f"File '{filename}' updated.")
                else:
                    print(f"File '{filename}' does not exist in your folder.")

        elif command.lower().startswith("search"):
            # Usage: search keyword
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: search <keyword>")
            else:
                keyword = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                found_files = []
                for root, dirs, files in os.walk(user_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as f:
                            content = f.read()
                            if keyword in content:
                                found_files.append(file_path)
                if found_files:
                    print("Files containing the keyword:")
                    for file in found_files:
                        print(file)
                else:
                    print(f"No files found containing the keyword '{keyword}'.")

        elif command.lower().startswith("upload_image"):
            # Usage: upload_image filename
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: upload_image <filename>")
            else:
                filename = parts[1]
                user_folder = os.path.join(os.getcwd(), current_user)
                file_path = os.path.join(user_folder, filename)
                if os.path.exists(file_path):
                    print(f"Image '{filename}' uploaded successfully.")
                else:
                    print(f"Image '{filename}' does not exist in your folder.")

        elif command.lower() == "shutdown":
            print("Shutting down DijonOS. Goodbye!")
            break            
        


        elif command.lower() == "BIOS":
            print("BIOS is a low-level software that initializes hardware during the booting process.")
            print("It performs POST (Power-On Self Test) to check hardware components and loads the operating system.")
            print("DijonOS is now running on top of the BIOS layer.")
            time.sleep(1)
            def bios_menu():
                bios_logging_enabled = True
                while True:
                    print("\n=== DijonOS BIOS ===")
                    print("1. Toggle System Logging (currently: {})".format("Enabled" if bios_logging_enabled else "Disabled"))
                    print("2. Delete a User Account")
                    print("3. List All User Accounts")
                    print("4. Exit BIOS")
                    choice = input("Select an option (1-4): ")
            
                    if choice == "1":
                        bios_logging_enabled = not bios_logging_enabled
                        print(f"System logging is now {'enabled' if bios_logging_enabled else 'disabled'}.")
                    elif choice == "2":
                        if not os.path.exists("accounts.txt"):
                            print("No accounts to delete.")
                            continue
                        username = input("Enter the username to delete: ")
                        found = False
                        # Remove user from accounts.txt
                        with open("accounts.txt", "r") as acc_file:
                            lines = acc_file.readlines()
                        with open("accounts.txt", "w") as acc_file:
                            for line in lines:
                                if line.strip() and line.split(":", 1)[0] != username:
                                    acc_file.write(line)
                                else:
                                    found = True
                        # Remove user folder
                        user_folder = os.path.join(os.getcwd(), username)
                        if os.path.exists(user_folder):
                            try:
                                for root, dirs, files in os.walk(user_folder, topdown=False):
                                    for name in files:
                                        os.remove(os.path.join(root, name))
                                    for name in dirs:
                                        os.rmdir(os.path.join(root, name))
                                os.rmdir(user_folder)
                                print(f"User folder '{username}' deleted.")
                            except Exception as e:
                                print(f"Error deleting user folder: {e}")
                        if found:
                            print(f"Account '{username}' deleted.")
                            if bios_logging_enabled:
                                with open("log.txt", "a") as log_file:
                                    log_file.write(f"Account '{username}' deleted via BIOS at {time.ctime()}\n")
                        else:
                            print(f"Account '{username}' not found.")
                    elif choice == "3":
                        if not os.path.exists("accounts.txt"):
                            print("No accounts found.")
                        else:
                            print("User accounts:")
                            with open("accounts.txt", "r") as acc_file:
                                for line in acc_file:
                                    if ":" in line:
                                        print(" -", line.split(":", 1)[0])
                    elif choice == "4":
                        print("Exiting BIOS...")
                        break
                    else:
                        print("Invalid option. Please select 1-4.")
            
            # Add this to your command loop:
            
            bios_menu()

        else:
            print(f"Command '{command}' not recognized. Type 'help' for available commands.")