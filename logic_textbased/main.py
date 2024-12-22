#Importing functions from other files
    #inputs.py - script for input handling
    #functions.py - script for logic
    #render.py handl - script for action and decision logic

from inputs import userfunc
from render import run_progress_bar, title_card
from inputs import first_option

#Recursion call stack
#import sys
#sys.setrecursionlimit(99999999999999)

#Variables used for data handlings:
    #user
    #betIN
    #betVAL

    #Card_Randomizer, Card_values
    #dealrandom1, dealrandom2, Dealval1, Dealerval2, DealerSum
    #Playrandom1, Playrandom2, Playerval1, Playerval2, PlayerSum

    #card_art, card_art_numeric

def main():
    userfunc() #ask for user name 
    run_progress_bar() #loading screen
    print()
    print()
    title_card() #Intro
    first_option() #Main menu
    

# if we are running in the main file, then call main()
# __name__ is a dir() attribute that assigns a file as a main file to which file it is declared.
if __name__ == "__main__":
    main()