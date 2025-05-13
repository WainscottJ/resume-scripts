#!/usr/bin/python3
#Name: Jacob Wainscott
#Date: 4/20/2025
#CIT 383 Module 9 assignment 1 User account Management
import argparse
import subprocess
import sys
import crypt
import getpass
import pwd
import random
import string

#This function creates or adds a new user account
#Checks if there is already a user
#Requires --username and --fullname
#Generates a strong password if none is provided
#Accepts an optional password if user wants to create their own
def create_user(username: str, fullname: str, password: str = None) -> None:
    try:
        # Check if the user already exists
        pwd.getpwnam(username)
        print(f"Error: User '{username}' already exists.")
        return
    except KeyError:
        pass  # User does not exist, continue

    if password is None:
        # Prompts the user for a password
        password = getpass.getpass("Enter password for the new user: ")

        # If a user leaves it blank this will generate a strong password
        #The item that could be improved here is the punctuation of adding only specific ones but this still good for now
        if not password:
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(12))
            print(f"Generated password for {username}: {password}")
#Important note here is that crypt is depreciated so there will be a message at output
    try:
        # Encrypt the password
        enc_passwd = crypt.crypt(password)

        # Construct the useradd command
        cmd = ['useradd', '-p', enc_passwd, '-c', fullname, username]

        # Run the useradd command
        subprocess.run(cmd, check=True)
        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to add user.")
        sys.exit(1)

#Deletes a user and needed 3 things
#Require --username
#Remove the user account and their home directory
#Handle the case where the user doesn't exist
def delete_user(username: str) -> None:
    try:
        # Check if the user exists
        pwd.getpwnam(username)
    except KeyError:
        print(f"Error: User '{username}' does not exist.")
        return

    try:
        # Delete the user and remove their home directory (-r)
        #Also the stdeer=subprocess.DEVNULL hides the error of items like mail spool and home directory not found to delete
        #Which can be found on docs.python.org/3/library/subprocess.html
        subprocess.run(['userdel', '-r', username], check=True, stderr=subprocess.DEVNULL)
        print(f"User '{username}' deleted successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to delete user.")
        sys.exit(1)

#Modifies an existing user and supports modifications like lock and add_root
def modify_user(username: str, lock: bool = False, new_fullname: str = None, add_root: bool = False) -> None:
    try:
        # Check if the user exists
        pwd.getpwnam(username)
    except KeyError:
        print(f"Error: User '{username}' does not exist.")
        return

    # Lock the user account
    if lock:
        try:
            subprocess.run(['usermod', '-L', username], check=True)
            print(f"User '{username}' has been locked.")
        except subprocess.CalledProcessError:
            print("Error: Failed to lock the account.")

    # Change the full name
    # The command for this is --modify --username <username>  --fullname "<change name>"
    if new_fullname:
        try:
            subprocess.run(['chfn', '-f', new_fullname, username], check=True)
            print(f"User '{username}' full name changed to '{new_fullname}'.")
        except subprocess.CalledProcessError:
            print("Error: Failed to change full name.")

    # Add user to root group
    if add_root:
        try:
            subprocess.run(['usermod', '-aG', 'root', username], check=True)
            print(f"User '{username}' added to root group.")
        except subprocess.CalledProcessError:
            print("Error: Failed to add user to root group.")

#Command line argument handling this functions implements the mutually exclusive flags and used the argparse module
def handle_arguments() -> None:
    parser = argparse.ArgumentParser(description="User Management")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--create', action='store_true', help="Create a new user")
    group.add_argument('--delete', action='store_true', help="Delete a user")
    group.add_argument('--modify', action='store_true', help="Modify a user")


    parser.add_argument('--username', type=str, help="Username of the account")
    parser.add_argument('--password', type=str, help="Password of the account")
    parser.add_argument('--fullname', type=str, help="Full name of the account")

    #These are the optional arguments that were listed in task 1
    parser.add_argument('--lock', action='store_true', help="Lock the account")
    parser.add_argument('--add_root', action='store_true', help="Add the root user to the account")

    args = parser.parse_args()
    if args.create:
        if not args.username or not args.fullname:
            print("Error: --username and --fullname are required for user creation.")
            sys.exit(1)
        create_user(args.username, args.fullname, args.password)

    elif args.delete:
        if not args.username:
            print("Error: --username is required for user deletion.")
            sys.exit(1)
        delete_user(args.username)

    elif args.modify:
        if not args.username:
            print("Error: --username is required for user modification.")
            sys.exit(1)
        modify_user(
            username=args.username,
            lock=args.lock,
            new_fullname=args.fullname,
            add_root=args.add_root
        )


if __name__ == "__main__":
    handle_arguments()
