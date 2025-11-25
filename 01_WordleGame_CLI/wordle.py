
"""wordle game :
   1 we take user inputs as five letters 
   2 we check those letters with our answer
   3 we check the position of letters with our answer letters
   4 we keep the user to continue till he guesses the answer
 
"""

from wonderwords import RandomWord
from colorama import Fore, init


init(autoreset=True)

RED_BACKGROUND = '\033[41m'
YELLOW_BACKGROUND = '\033[43m'
GREEN_BACKGROUND = '\033[42m'
RESET = '\033[0m'


def help():
    help_text = '''
    '''
    print(help_text)
    
def generate_random_word():
    r = RandomWord()
    answer = r.word(word_min_length=5, word_max_length=5) 
    return answer

def main():
    
    print(Fore.CYAN + " <<<<<<<<< WELCOME TO WORDLE  >>>>>>>>>")
    answer = list(generate_random_word())
    

    yellow = set()
    red = set()
    green = []
        
    while True:

        print(answer)
        
        input_letters = input(Fore.CYAN + f"Kindly add five letter word > " + RESET)

        if input_letters == "q" or input_letters == "Q":                                                                      # user wanna quit game
            print(f"Exiting program | Correct word was ".join(answer))
            break
        
        if len(input_letters) != 5:
            print(Fore.RED + "PLease enter 5 letter word only")
            continue
        
        for index, char in enumerate(input_letters):
            
            if char == answer[index]:                     
                print(Fore.GREEN + char + RESET, end=" ")                                         # if char and index is matching then its correct char at correct posi
                green.append(char)
                
            elif char in answer:                      
                print(Fore.YELLOW + char + RESET, end=" ")                                        # if char is in input then its there but at wrong place
                yellow.add(char)
                
            else:                                  
                print(Fore.RED + char + RESET, end=" ")                                           # char itself isnt in input means wrong char
                red.add(char) 


        # displaying
        
        # print("\n")
        print(f"{GREEN_BACKGROUND} CORRECT LETTERS {RESET} >>> {green}")
        print(f"{YELLOW_BACKGROUND} MISPLACED LETTERS {RESET} >>> {sorted(yellow)}")
        print(f"{RED_BACKGROUND} WRONG LETTERS {RESET} >>> {sorted(red)}")
        # print("\n")

        # win condition
        
        if green == list(answer):
            print(Fore.GREEN + "Correct")
            break

if __name__ == "__main__":
    main()