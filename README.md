# DijonOS
DijonOS is a beginner-friendly, text-based operating system simulation written in Python. It features:

* User Accounts: Users can create accounts with secure (hashed) passwords. Each user has a personal folder for their files.
Login System: Only users with correct credentials can access the system.
* File Management: Users can create, view, edit, delete, and rename text files within their own folders. They can also search for keywords in their files and simulate image uploads.
* Logging: System events (like logins and account creation) are recorded in a main log file, which can be viewed from the command line.
* BIOS Menu: An interactive BIOS menu allows toggling system logging, listing all user accounts, and deleting accounts (including their folders and credentials).
* Command Interface: DijonOS provides a command-line interface with helpful commands such as help, exit, shutdown, whoami, log, clear, create, delete, rename, view, edit, search, upload_image, and bios.
* Beginner Focus: The code is structured and commented for easy understanding and modification by beginners.
DijonOS is a great learning project for understanding basic OS concepts, user authentication, file operations, and command-line interfaces in Python.

# Update - Log. 
---------------
# 7-20-25 (Beta release 0.1)

DijonOS is created with very basic and limited options on use. 
# basic commands added (7/20/25): 
* help
* exit
* shutdown
* whoami
* log
* clear
* create <filename>
* delete <filename>
* rename <old_filename> <new_filename>
* view <filename>
* edit <filename>
* search <keyword>
* upload_image <filename>
* BIOS
