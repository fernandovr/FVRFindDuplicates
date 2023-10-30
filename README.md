<h1 align="center"><strong>FVRFindDuplicates</strong></h1>

# About
Python script to search for duplicate files on the computer.

Developed in version: Python 3.11.4

## Files
The two scripts do the same thing, the difference is that one is in Portuguese and the other in English.

`FVRFindDuplicates_en_US.py` -> Script entirely in English with comments for learning.

`FVRFindDuplicates_pt_BR.py` -> Script totalmente em Português com comentários para aprendizado.

## Installing Dependencies
Enter the command below at the command prompt in the directory where the *requirements.txt* file is located to install the dependencies required for this project.
```bash
pip install -r requirements.txt
```

## Converting to executable program

1. Install PyInstaller:

   Open a terminal or command prompt and run the following command to install PyInstaller with pip:

   ```bash
   pip install pyinstaller
   ```

2. Create the executable:

   In the terminal or command prompt, navigate to the directory where your Python script is located and run the following command to create the executable:

   ```bash
   pyinstaller --onefile your_script.py
   ```

   Replace "your_script.py" with the name of your Python file.

   PyInstaller will create a folder called "dist" in the same directory where your script is located, and inside that folder, you will find the Windows executable.
