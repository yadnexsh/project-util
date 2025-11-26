import sys
from wonderwords import RandomWord
from colorama import Fore, init

# COLOROMA BLOCKS
init(autoreset=True)
RED_BACKGROUND = '\033[41m'
YELLOW_BACKGROUND = '\033[43m'
GREEN_BACKGROUND = '\033[42m'
RESET = '\033[0m'


def help():
    help_text = """
WORDLE - Terminal Version
-------------------------
A simple word-guessing game.

Usage:
    python wordle.py [--start] [--settings] [--help]

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

    while settings_done == False:


        print("----SETTINGS MODE----")
        print(Fore.CYAN + f"Default settings : Attempts {attempts} | Word Length = {word_length}")
        print(Fore.CYAN + f"Max settings : Attempts {max_attempts} | Word Length = Max >{max_word_length} , Min > {min_word_length} ")
        input_settings = input("Settings\n[1] Attempts\n[2] Word Length\n[Q] Quit\n[D]Done\nChoose > ")

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

    input_word = ""
    while input_word != generated_word:

        input_word = input(Fore.CYAN + f"Kindly give {word_length} letter word > ")

        if "--quit" == input_word:
            print(f"Existing program | Random word > {generated_word} | Attempts > {attempts}")
            sys.exit(1)

        if len(input_word) != word_length:
            print(Fore.RED + "PLease enter 5 letter word only")
            continue

        for index, char in enumerate(input_word):

            if char == generated_letters[index]:
                print(Fore.GREEN + char + RESET , end=" ")                     # end="" skips \n and prints in line
                correct_letters.add(char)

            elif char in generated_letters:
                print(Fore.YELLOW + char + RESET , end=" ")
                misplaced_letters.add(char)

            else:
                print(Fore.RED + char + RESET , end=" ")
                wrong_letters.add(char)

        guessed += 1

        print("\n")
        print(f"{GREEN_BACKGROUND} CORRECT LETTERS {RESET} >>> {sorted(correct_letters)}")
        print(f"{YELLOW_BACKGROUND} MISPLACED LETTERS {RESET} >>> {sorted(misplaced_letters)}")
        print(f"{RED_BACKGROUND} WRONG LETTERS {RESET} >>> {sorted(wrong_letters)}")
        print("\n")
        print(Fore.CYAN + f"Attempts {guessed}")

    # Attempts check
        if attempts > 5 and guessed >= (attempts - 2):
            print("Wanna quit ? use \"--quit\" \n ")
        if guessed == attempts:
            print(Fore.CYAN + f"Better luck next time ! | Random word > " + Fore.GREEN + generated_word + Fore.CYAN + " | Attempts > " + Fore.YELLOW + str(attempts))
            sys.exit(1)

        if input_word == generated_word:
            print(Fore.GREEN + f"Congrats you have guessed it : {generated_word}")

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