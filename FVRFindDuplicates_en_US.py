import os  # Module for interacting with the operating system, such as navigating directories and checking for file and directory existence.
import hashlib  # Module for hash calculations (in the code, it's used to calculate the SHA-256 hash of files).
import shutil  # Module for high-level file and directory operations, such as copying and removal.
import win32com.client  # Module for accessing COM objects on Windows (in the code, it's used to create shortcuts in the system).
import re  # Module for working with regular expressions, used to clean file names.
import keyboard  # Module for monitoring keyboard events, used to wait for the Enter key to be pressed at the end.
from colorama import Fore, Back, Style, init  # Module that provides functionality for coloring console output.

# Initialize the colorama module with the option autoreset=True, which means color settings are automatically reset after each colored output.
init(autoreset=True)

# Program header art. It's a multiline string that will be printed at the beginning of the program.
header_text = """
                                                      
        :==:                              :==:        
     =********=                        :********+     
    ************                      ************.   
   +*************                    +************=   
   +*************+                  =*************+   
   .**************-                :**************:   
    .**************-              :**************:    
     :**************:            :**************-     
      =**************            **************+      
       =**************.         ***************       
        ***************        ***************        
         ***************      ***************         
          ***************    +**************          
          .**************=  :**************.          
            **************=:**************:           
            :****************************:            
             -***************###########=             
              -***************#########=              
               ***************%%%%%%%%*               
                ***************%%%%%%*                
                 *############**%%%%*                 
                 .*#############*%%#.     Viappz.com           
                   *##############%.        by Fernando VR          
                   :#############*:                   
                    :############=                    
                     :##########-                     
                       =*#####=                       
                                                      
"""

# Print the colored header
print(Fore.GREEN + Back.BLACK + header_text)

# Get the width of the terminal in columns, which will be used later to limit the size of some text outputs.
terminal_width = shutil.get_terminal_size().columns

# This function checks the size of the text, and if it's larger than the terminal width, it truncates it and adds "..." at the end.
def limit_text_size(text):
    if len(text) > terminal_width:
        return text[:terminal_width - 3] + "..."  # Truncate the text and add "..."
    return text

# This function clears the current line in the console by filling it with white spaces.
def clear_line():
    print(" " * terminal_width, end="\r")

# This function calculates the SHA-256 hash of a file.
def calculate_file_hash(file_path):
    # Create a hash object
    sha256 = hashlib.sha256()

    # Read the file in chunks to avoid excessive memory consumption
    with open(file_path, "rb") as f:
        while True:
            block = f.read(4096)
            if not block:
                break
            sha256.update(block)

    # Return the calculated hash
    return sha256.hexdigest()

# This function finds duplicate files in a directory and its subdirectories.
def find_duplicate_files(directory):
    # Dictionary to store hashes and corresponding files
    hash_files = {}

    for root_folder, subdirectories, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root_folder, file)
            file_hash = calculate_file_hash(full_path)

            if file_hash in hash_files:
                hash_files[file_hash].append(full_path)
            else:
                hash_files[file_hash] = [full_path]

            # Clear the current line in the console
            clear_line()

            limited_file_name = limit_text_size(f"Analyzing: {file}")

            # Display the file being analyzed
            print(Fore.CYAN + limited_file_name, end="\r")

    clear_line()
    print(Fore.GREEN + "Analysis completed.")

    # Return the duplicate files
    return {hash: files for hash, files in hash_files.items() if len(files) > 1}

# This function cleans a file name by removing special characters and limiting it to 50 characters.
def clean_file_name(original_file):
    file_name = os.path.splitext(os.path.basename(original_file))[0]  # Get the file name without the extension
    file_name = re.sub(r"[^\w\s]", "", file_name)  # Remove special characters using regular expressions
    file_name = file_name.strip()[:50]  # Limit to 50 characters
    return file_name

# This function creates a name for a shortcut based on the original file and counters.
def create_shortcut_name(original_file, destination_folder, overall_counter, duplicates_counter):
    _, extension = os.path.splitext(original_file)

    # Remove special characters from the file name and limit it to 50 characters
    file_name = clean_file_name(original_file)

    # Format the name by adding a 5-digit overall count and a 3-digit count for each duplicate file of the same type
    shortcut_name = f"{overall_counter:05d}-{duplicates_counter:03d}-{file_name}{extension}"
    return shortcut_name

# This function creates a Windows shortcut for an original file.
def create_windows_shortcut(original_file, destination_folder, overall_counter, duplicates_counter):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_name = create_shortcut_name(original_file, destination_folder, overall_counter, duplicates_counter)
    shortcut = shell.CreateShortcut(os.path.join(destination_folder, shortcut_name + ".lnk"))
    shortcut.TargetPath = original_file
    shortcut.save()

# This function prompts the user for a valid directory path and ensures that it is valid.
def get_valid_directory():
    while True:
        base_directory = input("Enter the directory path to search: ")
        if not base_directory:
            print(Fore.YELLOW + "The field cannot be blank. Please provide a valid directory.")
        elif not os.path.exists(base_directory):
            print(Fore.RED + f"The directory '{base_directory}' does not exist. Please provide a valid directory.")
        else:
            return base_directory

# Main block of the program
# The main block of the program is executed only if the code is run as a script, not if it's imported as a module.
if __name__ == "__main__":

    # Get the base directory to search from the get_valid_directory function.
    base_directory = get_valid_directory()

    if base_directory is None:
        # Executes if the base_directory is not provided.
        # This line will likely never be executed, but it's here just for assurance to avoid any errors in the project.
        # I considered creating a monitoring here for when the user presses the ESC key on the keyboard to end the program, but it would require creating a new thread, so I decided not to make the program heavier just for a key, considering the user can end it by closing the terminal.
        print("Program finished.")
    else:
        # Call the find_duplicate_files function to find duplicate files in the base directory.
        duplicate_files = find_duplicate_files(base_directory)

    # Create a destination folder for shortcuts if it doesn't exist yet.
    destination_folder = "Duplicate_Shortcuts"
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    # In a loop, iterate over the found duplicate files and create shortcuts for them.
    overall_counter = 1
    for hash, files in duplicate_files.items():
        duplicates_counter = 1
        for file in files:
            print(Fore.RED + f"Duplicate file with hash {hash}:")
            print(Fore.MAGENTA + f"  {file}")
            create_windows_shortcut(file, destination_folder, overall_counter, duplicates_counter)
            duplicates_counter += 1
        overall_counter += 1

    # Print a message indicating that the shortcuts have been successfully created.
    print(Fore.GREEN + f"Shortcuts for duplicate files have been created in {os.path.abspath(destination_folder)}")

    # Display a completion message and wait for the user to press the Enter key to close the program.
    print(Fore.YELLOW + "Finished. Press ENTER to exit.")
    keyboard.wait("enter")