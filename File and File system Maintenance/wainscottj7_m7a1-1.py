#!usr/bin/python3
#Name: Jacob Wainscott
#Date: 3/30/2025
#Module 7 Assignment 1 Files and File system maintenance
import os

#Creates the specified number of files with a given prefix and extension inside the specified directory.
def create_files(file_name_prefix: str, num_of_files: int, directory: str, file_extension: str):
    for i in range(1, num_of_files + 1):
        while True:
            #Prompts the user for a file name
            user_file_name = input(f"Enter a name for file {i} (without extension): ")
            file_name = f"{user_file_name}.{file_extension}"
            file_path = os.path.join(directory, file_name)

            #Check if the file already exists
            # Also makes sure that whether something is lower case or upper that it cant be used if same word
            if any(existing_file.lower() == file_name.lower() for existing_file in os.listdir(directory)):
                print(f"File '{file_name}' already exists. Please choose another name.")
            else:
                #Create the file and write a test message into it
                with open(file_path, "w") as file:
                    file.write(f"This is file number {i} with name '{user_file_name}' and extension '{file_extension}'.")
                print(f"File '{file_name}' created.")
                break



#Creates a directory if it doesn't exist.
def create_dir(name_of_directory: str):

    if not os.path.exists(name_of_directory):
        os.makedirs(name_of_directory)
        print(f"Directory '{name_of_directory}' created.")
    else:
        print(f"Directory '{name_of_directory}' already exists.")

#Renames the specified file to the new name provided.
def rename_file(filename: str, new_name: str):
    #Check if new name already exists before renaming to avoid overwriting
    if os.path.exists(new_name):
        print(f"Error: File '{new_name}' already exists.")
        return
    if os.path.exists(filename):
        os.rename(filename, new_name)
        print(f"File '{filename}' renamed to '{new_name}'.")
    else:
        print(f"File '{filename}' does not exist.")


#Display Directory Contents
def display_contents(directory_name: str):

    try:
        #List all files and directories in the specified directory
        for entry in os.listdir(directory_name):
            entry_path = os.path.join(directory_name, entry)
            if os.path.isdir(entry_path):
                print(f"{entry} - Directory")
            else:
                print(f"{entry} - File")
    except FileNotFoundError:
        print(f"The directory '{directory_name}' does not exist.")

#Rename Files in Directory
def rename_files_in_directory(target_directory: str, current_ext: str, new_ext: str):
    #Allowed file extensions
    valid_extensions = ['txt', 'png', 'doc', 'dat']


    #Check if current extension is valid
    if current_ext not in valid_extensions:
        print(f"Error: '{current_ext}' is not a valid extension. Allowed extensions are: txt, png, doc, dat.")
        return


    #Check if new extension is valid
    if new_ext not in valid_extensions:
        print(f"Error: '{new_ext}' is not a valid extension. Allowed extensions are: txt, png, doc, dat.")
        return


    #Skip renaming if the current and new extensions are the same
    if current_ext == new_ext:
        print(f"Extensions are the same. No files will be renamed.")
        return


    try:
        #Loops through the files in the target directory
        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)


            #Check if it's a file and if the file has the current extension
            if os.path.isfile(file_path) and filename.endswith(current_ext):
                # Generate the new filename with the new extension
                new_filename = filename.replace(current_ext, new_ext)
                new_file_path = os.path.join(target_directory, new_filename)


                #Rename the file
                os.rename(file_path, new_file_path)
                print(f"File '{filename}' renamed to '{new_filename}'.")


    except FileNotFoundError:
        print(f"The directory '{target_directory}' does not exist.")




#Main function that handles all tasks.
def main():

    #Prints the name of the current working directory.
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    #Create a directory named CITFall2023<username> in home directory of the user.
    username = os.getlogin()
    home_dir = os.path.expanduser("~")  # Get the user's home directory
    new_directory = os.path.join(home_dir, f"CITFall2023{username}")
    create_dir(new_directory)

    #Prompts the user for the number of files and their extension and create files.
    while True:
        try:
            num_files = int(input("Enter the number of files to create: "))
            if num_files <= 0:
                print("Please enter a positive number for the number of files.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    valid_extensions = ['txt', 'png', 'doc', 'dat']
    while True:
        file_extension = input(f"Enter the file extension ({', '.join(valid_extensions)}): ").strip().lower()
        if file_extension in valid_extensions:
            break
        else:
            print("Invalid extension. Please choose from: txt, png, doc, dat.")

    file_name_prefix = f"file_{username}_"
    create_files(file_name_prefix, num_files, new_directory, file_extension)

    #Prompts the user for a new extension
    #Also checks to make sure valid extensions are used if not ask user to type again
    while True:
        new_ext = input("Enter the new file extension to rename the files to: ").strip().lower()
        if new_ext in valid_extensions:
            break
        else:
            print("Invalid extension. Please choose from: txt, png, doc, dat.")

    rename_files_in_directory(new_directory, file_extension, new_ext)

    #Display the contents of the directory.
    display_contents(new_directory)

if __name__ == "__main__":
    main()



