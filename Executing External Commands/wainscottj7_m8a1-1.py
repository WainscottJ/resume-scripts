#!/usr/bin/python3
#Name:Jacob Wainscott
#Module 8 Assignment 1
#Date: 4/5/2025


import os
import sys
import shutil
import subprocess
import tarfile
import zipfile


#Backs up the contents of one directory to another using the rsync command
def back_up_dir(dir_path: str, dest_path: str):
    if not os.path.isdir(dir_path):
        print(f"Error: Source directory '{dir_path}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(dest_path):
        print(f"Error: Destination directory '{dest_path}' does not exist.")
        sys.exit(1)
    try:
        subprocess.run(['rsync', '-av', dir_path + '/', dest_path], check=True)
        print(f"Backup completed from '{dir_path}' to '{dest_path}'.")
    except subprocess.CalledProcessError as error:
        print(f"Error during rsync: {error}")
        sys.exit(1)


#Creates an archive (e.g., .zip, .tar.gz) of the specified directory and saves it to the user’s home directory.
def archive_dir(dir_name: str, arch_type: str, archive_base_name: str):
    valid_types = ['zip', 'gztar', 'tar', 'bztar', 'xztar']
    if arch_type not in valid_types:
        print(f"Error: Invalid archive type '{arch_type}'. Valid types are: {', '.join(valid_types)}")
        return
    if not os.path.isdir(dir_name):
        print(f"Error: Directory '{dir_name}' does not exist.")
        return
    home_directory = os.path.expanduser('~')
    archive_path = os.path.join(home_directory, archive_base_name)
    try:
        archive_full_path = shutil.make_archive(archive_path, arch_type, root_dir=dir_name)
        print(f"Archive created at: {archive_full_path}")
    except Exception as error:
        print(f"Error creating archive: {error}")


# Reads the contents of a .zip or .tar.* archive and lists any files larger
# than the threshold size (in KB).
def get_large_archive(zip_file_path: str, threshold: int):
    if not os.path.isfile(zip_file_path):
        print(f"Error: File '{zip_file_path}' does not exist.")
        return
    print(f"Checking archive: {zip_file_path}")
    print(f"Threshold: {threshold} KB")
    try:
        if zip_file_path.endswith('.zip'):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                comment = zip_file.comment.decode('utf-8') if zip_file.comment else "Unknown"
                print("Archive created on OS:", comment)
                print("Files larger than threshold:")
                for file_info in zip_file.infolist():
                    file_size_kb = file_info.file_size / 1024
                    if file_size_kb > threshold:
                        print(f"{file_info.filename} - {file_size_kb:.2f} KB")
        elif zip_file_path.endswith(('.tar.gz', '.tar', '.tar.bz2', '.tar.xz')):
            with tarfile.open(zip_file_path, 'r') as tar_file:
                print("Archive contents:", tar_file.getnames())
                print("Files larger than threshold:")
                for member in tar_file.getmembers():
                    file_size_kb = member.size / 1024
                    if file_size_kb > threshold:
                        print(f"{member.name} - {file_size_kb:.2f} KB")
        else:
            print("Unsupported archive format.")
    except Exception as error:
        print(f"Error reading archive: {error}")


#Displays files modified in the last 30 days using the find command.
def show_recently_modified_files(directory_path: str = None):
    #Checking if no directory was given or if path is invalid, then use current working directory
    if directory_path is None or not os.path.isdir(directory_path):
        directory_path = os.getcwd()
    print(f"Searching for recently modified files in: {directory_path}")
    try:
        subprocess.run(['find', directory_path, '-type', 'f', '-mtime', '-30'], check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error using find command: {error}")


#Menu that allows the user to interactively select one of the 4 features or exit the script
def menu():
    while True:
        print("\nSystem Admin Menu")
        print("Note: When entering paths, use the full path (e.g., /home/student/foldername)")
        print("Also note that when doing archives to put extension at the end like /home/student/sourcez.zip")
        print("1. Back up a directory")
        print("2. Archive a directory")
        print("3. List large files in an archive")
        print("4. Show recently modified files")
        print("5. Exit")


        user_choice = input("Enter your choice (1-5): ")
        if user_choice == '1':
            source = input("Enter source directory: ")
            destination = input("Enter destination directory: ")
            back_up_dir(source, destination)
        elif user_choice == '2':
            directory_to_archive = input("Enter directory to archive: ")
            archive_type = input("Enter archive type (zip, gztar, tar, bztar, xztar): ")
            base_name = input("Enter base name for archive: ")
            archive_dir(directory_to_archive, archive_type, base_name)
        elif user_choice == '3':
            archive_path = input("Enter archive file path: ")
            try:
                size_threshold = int(input("Enter file size threshold (KB): "))
                get_large_archive(archive_path, size_threshold)
            except ValueError:
                print("Invalid threshold. Must be an integer.")
        elif user_choice == '4':
            recent_dir = input("Enter directory (or press Enter for current dir): ")
            show_recently_modified_files(recent_dir.strip() or None)
        elif user_choice == '5':
            print("Exiting. Thanks for using our menu system!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    menu()





