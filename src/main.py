import sys
from wonderwords import RandomWord
from colorama import Fore, init


init(autoreset=True)



# ---------------- COLORS ----------------
CYAN = Fore.CYAN
RED = Fore.RED
GREEN = Fore.GREEN
MAGENTA = Fore.MAGENTA
YELLOW = Fore.YELLOW


# ---------------- HELP ----------------
def help_menu():
    print("""

WORDLE - Terminal Edition
------------------------
Flags:
  --start      Start game
  --settings   Configure attempts & length
  --help       Show help
  
In game:
  --quit       Exit

""")
    
    
# -------------- SETTING MODE --------------
def settings_mode():
    attempts = 5
    word_length = 5
    MAX_ATTEMPTS = 10
    MIN_LEN = 5
    MAX_LEN = 8
    
    
    while True:
        print("\n---- SETTINGS ----")
        print(f"1. Attempts ({attempts})")
        print(f"2. Word Length ({word_length})")
        print("d. Done")
        print("q. Quit")
        
        choice = input("Choose > ").lower()
        
        # --- Attempts Logic --------
        
        if choice == "1":
            while True:
                try:
                    val = int(input("Attempts > "))
                    if 1 <= val <= MAX_ATTEMPTS:
                        attempts = val
                        break
                    print(RED + f"Range: 1 - {MAX_ATTEMPTS}")
                except ValueError:
                    print(RED + "Numbers only")
                    
        # ----- Word Length Logic ----------
        
        elif choice == "2":
            while True:
                try:
                    val = int(input("Word length > "))
                    if MIN_LEN <= val <= MAX_LEN:
                        word_length = val
                        break
                    print(RED + f"Range: {MIN_LEN} - {MAX_LEN}")
                except ValueError:
                    print(RED + "Numbers only")
                    
        elif choice == "d":
            return attempts, word_length            # Returning default values
        
        elif choice == "q":
            sys.exit()
            
        else:
            print("Invalid option")


# ------- CHECKING LOGIC -----------

def checker(guess, target):
    """
    Docstring for checker :
    The given func. checks the guess words each letter and compares with each letter of targeted word, based on that it creates a flag for it.
    Flags are getting stored in result - which we will be using in other func further below.
    
    Example:
        guess  = "plate"
        target = "apple"
        
        Result:
            ['yellow', 'yellow', 'green', 'red', 'green']
    
    :param guess: Input word from user is guess.
    :param target: Randomly chosen word from Lib is target
    """
    
    result = []
    
    for i, ch in enumerate(guess):
        if ch == target[i]:
            result.append("green")
        elif ch in target:
            result.append("yellow")
        else:
            result.append("red")
            
    return result


def launcher(attempts, word_length):
    """
    Docstring for launcher
    The given func is a launcher which creates a random word , checks its none or not. Further on takes the result and stored flags on it and constructs the color coded output
    Plus has --quit and --help flags which we can use in answer to stop or to get help.
    :param attempts: attempts are coming from settings_menu()
    :param word_length: word_length is coming from settings_menu()
    """
    
    print(GREEN + f"\nSTARTING GAME | Attempts > {attempts} | Word Length > {word_length}")
    
    r = RandomWord()
    
    # safe generation
    generated_word = None
    while not generated_word:
        generated_word = r.word(word_min_length=word_length,
                                word_max_length=word_length)
        
    generated_word = generated_word.lower()
    
    guessed = 0
    
    misplaced_letters = set()
    wrong_letters = set()
    correct_letters = set()

    print(MAGENTA + "| -- | -- | WELCOME TO WORDLE | -- | -- |\n")

    while guessed < attempts:
        
        input_word = input(CYAN + f"Give {word_length} letter word > ").lower()         # Taking user input
        
        if input_word == "--quit":                                                      # Edge cases and flags
            sys.exit()
            
        if input_word == "--help":
            help_menu()
            continue
        
        if len(input_word) != word_length:
            print(RED + f"Enter {word_length} letters only")
            continue
        
        if not input_word.isalpha():
            print(RED + "Letters only")
            continue
        
        guessed += 1
        
        results = checker(input_word, generated_word)                       # Sending input word and generated word to checker() to check.
        
        for char, state in zip(input_word, results):                        # zip pairs the two list
            """
            Docstring for above loop.
            It takes the output from checker() , stores in results. (All flags)
            Takes each letter and ties with flag (zip) , based on flag it sorts the data in corresponding set.

            """
            if state == "green":
                print(GREEN + char, end=" ")
                correct_letters.add(char)
                misplaced_letters.discard(char)
                
            elif state == "yellow":
                print(YELLOW + char, end=" ")
                misplaced_letters.add(char)
                
            else:
                print(RED + char, end=" ")
                wrong_letters.add(char)
                
        print("\n")
        
        print(YELLOW + "MISPLACED >>>", sorted(misplaced_letters) or "None")
        print(GREEN + "CORRECT   >>>", sorted(correct_letters) or "None")
        print(RED + "WRONG     >>>", sorted(wrong_letters) or "None")
        print(CYAN + f"Attempts {guessed}/{attempts}\n")
        
        if input_word == generated_word:
            print(GREEN + f"Congrats! You guessed it: {generated_word}")
            return
        
    print(CYAN + f"Game Over! Word was: {generated_word}")


# ---------------- MAIN ----------------

def main():
    
    flags = sys.argv[1:]
    attempts = 5
    word_length = 5
    
    if not flags or "--help" in flags:
        help_menu()
        return
    
    if "--settings" in flags:
        attempts, word_length = settings_mode()
        
    launcher(attempts, word_length)
    
    
if __name__ == "__main__":
    main()