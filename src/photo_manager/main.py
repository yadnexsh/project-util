



import shutil
import sys 
import os
import re
from datetime import datetime
from colorama import Fore,init,Style

init(autoreset=True)


today = datetime.now().strftime("%Y-%m-%d")


def help():
    help_text = """Help text""" 
    print(help_text)
    
def setup_mode():
    print("---SETUP MODE---")
    print("Directory : A folder which you want to organize\nSubject : A theme or grp of photos you wanna organize")
    directory = input("[1] Directory > ")
    subject = input("[2] Subject > ")
    changes = input("[N] Do you wanna change anything ? > ")
    
    return directory , subject , changes

def list_files(directory):
    
    if not os.path.exists(directory):
        print(Fore.RED + f"'{directory}' not found.")
        sys.exit(0)

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        print(path)
        

def unique_subfolder(main_folder, sub):

    counter = 1
    while True:
        unique_name = f"{sub}{counter}"
        unique = os.path.join(main_folder, unique_name)
        if not os.path.exists(unique):
            return unique
        counter += 1
    
def organize_files(directory, dry_run=False):
    
    list_directory = os.listdir(directory)
    
    for folder in list_directory:
        src_folder = os.path.join(directory, folder)
        
        if not os.path.isdir(src_folder):
            continue                            # want to run a code if it stops on file
        
        split = re.split(r"\s*-\s*", folder)

        if len(split) == 2:
            main = split[0].strip()
            sub = split[1].strip()                                      # to remve space
            
            main_folder = os.path.join(directory, main)
            sub_folder = unique_subfolder(main_folder, sub)

            
            if dry_run:
                print(f"Code would make {main_folder} and {sub_folder}")
            else:
                os.makedirs(sub_folder, exist_ok=True)
            
            for item in os.listdir(src_folder):         # fetching item inside the folder to move
                source = os.path.join(src_folder , item)
                destination = os.path.join(sub_folder, item)
                if dry_run:
                    print(f"Code would move '{source}' > '{destination}'")
                else:
                    shutil.move(source, destination)

            if dry_run:
                print(f"Code Would remove folder > {src_folder}")
            else:
                os.rmdir(src_folder)
                
            print(f"{folder} > {sub_folder}")
            
            
        else:
            print(f"{folder} | Not Required")
            
def main():
    
    if len(sys.argv) < 2:                                       
        print(Fore.RED + "No directory provided.")
        help()
        sys.exit(1)
        
    directory = os.path.abspath(sys.argv[1])
    flags = sys.argv[2:]
    
    valid_flags = ["--help", "--ls", "--dry-run", "--organize"]


    
    if not flags:
        print(Fore.RED + "No action provided. Use --organize or -l.")
        help()
        sys.exit()
    

        
    for each in flags:
        if each not in valid_flags:
            print("Invalid flag" , each)
            print(f"Allowed flags are {valid_flags}")
            sys.exit(1)
    
    if not os.path.exists(directory):
        print(Fore.RED + f"'{directory}' not found.")
        sys.exit(1)

    if "--help" in flags:
        help()
        sys.exit(0)
        
    if "--ls" in flags:
        list_files(directory)
        sys.exit(0)
    
    if "--organize" in flags:
        dry_run = "--dry-run" in flags
        organize_files(directory, dry_run=dry_run)
        sys.exit(0)





    
if __name__ == "__main__":
    main()