import sys
from wonderwords import RandomWord
from colorama import Fore, init
import string


init(autoreset=True)

RESET = '\033[0m'


def help():
    help_text = """
WORDLE - Terminal Version
-------------------------
A simple word-guessing game.

Usage:
    python main.py [--start] [--settings] [--help]

Options:
    --start       Start the game with default settings (5 attempts, 5-letter word).
    --settings    Change attempts and word length before starting.
    --help        Show this help message.

In-Game:
    • Enter a word with the required length.
    • Colors show feedback:
         Green  = correct position
         Yellow = wrong position
         Red    = not in word
    • Type --quit to exit early.

Enjoy the game!
"""
    print(help_text)

def settings_mode():

    attempts = 5
    word_length = 5
    max_attempts = 10
    max_word_length = 8
    min_word_length = 5
    settings_done = False

    state = "Default Settings"
    
    while settings_done == False:


        print("----SETTINGS MODE----")
        
        print(Fore.CYAN + f"{state} : Attempts {attempts} | Word Length = {word_length}")
        
        print(Fore.CYAN + f"Max settings : Attempts {max_attempts} | Word Length = Max > {max_word_length} , Min > {min_word_length} ")
        
        print("Settings")
        print("[1] Attempts")
        print("[2] Word Length")
        print("[Q] Quit")
        print("[D] Done")
        input_settings = input("Choose > ")

        if "D" in input_settings or "d" in input_settings:
            print(Fore.GREEN + "Settings Done - Taking no more changes")
            settings_done = True

        if "q" == input_settings or "Q" == input_settings:
            print(Fore.RED + "Exiting")
            sys.exit(0)

        
        if "1" in input_settings:

            try:
                attempts = int(input("Attempts > "))

                if attempts >= max_attempts:
                    print(Fore.RED + f"Supported Max attempts : {max_attempts}")
                if attempts <= 0:
                    print(Fore.RED + "Zero and -ve numbers arent allowed")
                else:
                    state = "Changed Settings"

            except ValueError as e: 
                print(f"{e}")
            except Exception as e:
                    print(f"{e}")

        r =  RandomWord()
        if "2" in input_settings:
            try:
                word_length = int(input("Word length > "))
                if word_length >= max_word_length:
                    print(Fore.RED + f"Supported max word length : {max_word_length}")
                if word_length <= min_word_length:
                    print(Fore.RED + f"Required word length is {min_word_length}")
            except ValueError as e:
                print(f"{e}")
            except Exception as e:
                print(f"{e}")


    return attempts, word_length




def start_mode(attempts, word_length):

    print(Fore.GREEN + f"STARTING GAME | Attempts > {attempts} | Word Length > {word_length}")

    r = RandomWord()
    generated_word = r.word(word_min_length=word_length, word_max_length=word_length)
    generated_letters = list(generated_word)
    print(generated_word)
    guessed = 0
    misplaced_letters = set()
    wrong_letters = set()
    correct_letters = set()

    print(Fore.MAGENTA + "<><><> WELCOME TO WORDLE <><><>")

    all_letters = list(string.ascii_lowercase)
    unused_letters = all_letters.copy()
    
    input_word = ""
    while input_word != generated_word:

        input_word = input(Fore.CYAN + f"Kindly give {word_length} letter word > ")

        if "--quit" == input_word:
            print(f"Existing program | Random word > {generated_word} | Attempts > {attempts}")
            sys.exit(1)

        if "--help" == input_word:
            help()
            sys.exit(0)

        if len(input_word) != word_length:
            print(Fore.RED + f"PLease enter {word_length} letter word only")
            continue

        for index, char in enumerate(input_word):

            if char == generated_letters[index]:
                print(Fore.GREEN + char , end=" ")                     # end="" skips \n and prints in line
                correct_letters.add(char)
                misplaced_letters.discard(char)                         #.remove(elem) removes elem from the set but raises a KeyError if elem is not present in the set.
                if char in unused_letters:                              # .discard(elem) removes elem if present but does nothing and raises no error if elem is absent.
                    unused_letters.remove(char)

            elif char in generated_letters:
                print(Fore.YELLOW + char , end=" ")
                misplaced_letters.add(char)
                if char in unused_letters:
                    unused_letters.remove(char)
                
            else:
                print(Fore.RED + char , end=" ")
                wrong_letters.add(char)
                if char in unused_letters:
                    unused_letters.remove(char)
            

        guessed += 1

        print("\n")
        print(Fore.YELLOW + "CURRENTLY MISPLACED LETTERS >>>", sorted(misplaced_letters) or "None")
        print(Fore.GREEN + f"CORRECT LETTERS >>> {sorted(correct_letters) if correct_letters else 'None'}")
        print(Fore.RED + f"WRONG LETTERS >>> {sorted(wrong_letters) if wrong_letters else 'None'}")
        print(f"UNUSED LETTERS >>> {sorted(unused_letters)}")
        print(Fore.CYAN + f"Attempts {guessed}\n")

    # Attempts check
    
        if input_word == generated_word:
            print(Fore.GREEN + f"Congrats you have guessed it : {generated_word}")
            
        if attempts > 5 and guessed >= (attempts - 2):
            print("Wanna quit ? use \"--quit\" \n ")
            
        if guessed == attempts:
            print(Fore.CYAN + f"Better luck next time ! | Random word > " + Fore.GREEN + generated_word + Fore.CYAN + " | Attempts > " + Fore.YELLOW + str(attempts))
            sys.exit(1)

        

def main():

    flags = sys.argv[1:]

    attempts = 5
    word_length = 5

    valid_flags = ["--start" , "--settings"]


    if "--help" in flags:
        help()
        sys.exit(0)

    if not flags:
        help()
        sys.exit()

    for each in flags:
        if each not in valid_flags:
            print("Invalid flag" , each)
            print(f"Allowed flags are {valid_flags}")
            sys.exit(1)


    if "--settings" in flags:
        attempts , word_length = settings_mode()
        start_mode(attempts, word_length)
    elif "--start" in flags:
        start_mode(attempts, word_length)



if __name__ == "__main__":
    main()