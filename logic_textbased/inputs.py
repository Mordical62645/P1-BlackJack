import re #regex
import colorama 

#Ask for user name
def userfunc(): 
    global user
    print()
    print(colorama.Fore.GREEN+"What is your name, Player? ([0] to quit)")
    
    #Checkpoint for input validation
    while True: 
        user = input(colorama.Fore.WHITE+"> ")
        print()

        #Check for regex invalidity
        if not re.match(r'^[a-zA-Z\s]+$', user):
            
            #Exit point
            if user == "0":
                print(colorama.Fore.GREEN+"Hope to see you again, ",user +"!")
                print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
                exit()

            print(colorama.Fore.RESET+"INVALID. Please input a word/name/letter")
            continue
        
        print(colorama.Fore.GREEN+"Welcome, "+colorama.Fore.WHITE+user+colorama.Fore.GREEN+"!")
        break

#Main menu
def first_option():
    from functions import info
    print(colorama.Fore.GREEN+"[0] Bet")
    print("[1] More Info and Instructions")
    print("[2] Quit")

    #In case the input is False, continue
    while True:
        option_input = input(colorama.Fore.WHITE+"> ")

        #Convert option_input to integer and Value checking
        try: 
            option_input = int(option_input)

            #if input is less than or equal to -1 exceeded or equal to 3 then raise ValueError then continue to while True.
            if option_input <= -1 or option_input >= 3:
                raise ValueError
        
        except ValueError:
            print()
            print(colorama.Fore.RED+"INVALID. Please select from the given options")
            continue
        
        #betting starts
        if option_input == 0:
            print()
            first_bet() 
            break
        
        #view info
        elif option_input == 1:
            print()
            info() 
            break
        
        #exit point
        elif option_input == 2: 
            print(colorama.Fore.GREEN+"Hope to see you again, ",user +"!")
            print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
            exit()

#Call when lost. Choice to restart or quit.
def lose_options():
    print(colorama.Fore.GREEN+"[0] Restart")
    print("[1] Quit")
    print()

    #In case the input is False, continue
    while True:
        user_input = input(colorama.Fore.WHITE+"> ")

        #Convert user_input to integer and Value checking
        try: 
            user_input = int(user_input)

            #if input is less than or equals to 0 and higher or equals to 2, raise ValueError
            if user_input <= -1 or user_input >= 2:
                raise ValueError
        
        except ValueError:
            print()
            print(colorama.Fore.RED+"INVALID. Please select from the given options")
            print()
            continue
        
        #Restart
        if user_input == 0:
            print("----------------------------------------------------------------------------")
            first_bet()
            break
        
        #Quit
        elif user_input == 1:
            print(colorama.Fore.GREEN+"THANK YOU, ",user.upper()," FOR PLAYING!")
            print(colorama.Fore.LIGHTYELLOW_EX+"Made by Marco Tecson")
            print(colorama.Fore.GREEN+"BlackJack v.1.0.0")
            print("Made with Python")
            print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
            exit()

#Call when won. 
def re_bet(betIN, betVal): #Pass the current value and state of betIN and betVal
    #DEBUGGER print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
    from functions import game_start
    print(colorama.Fore.GREEN+"Place your bet ([0] to quit)")
    print()
    print("Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)
    print()
    
    #In case the input is False, continue
    while True:
        betIN = input(colorama.Fore.WHITE+"> ")
        print()
        
        #Convert betIN to integer and Value checking
        try:
            betIN = int(betIN)

            #exit point
            if betIN == 0:
                print(colorama.Fore.GREEN+"Hope to see you again, ",user +"!")
                print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
                exit()

            #Allowed betting ranged from 1 to the amount of current balance
            elif betIN <= betVal and betIN >= 1:
                betVal -= betIN 
                print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
                print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)
                
                print()
                #DEBUGGER print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
                game_start(betIN, betVal)
                break
        
            elif betIN <= -1:
                print(colorama.Fore.RED+"not enough balance")
                continue

            else:
                raise ValueError

        except ValueError:
            print(colorama.Fore.RED+"INVALID. Please input a number/integer")
            print()
            continue

#First betting with default balance of 500
def first_bet():
    from functions import game_start

    #Declaration of 2 main variable that will be passed
    global betIN
    global betVal

    #Assigned for first betting (the first round of the game)
    betVal = 500

    print(colorama.Fore.GREEN+user,"got"+colorama.Fore.WHITE,"500"+colorama.Fore.GREEN,"for starters!")
    print("Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)
    print()
    print("How much do you want to bet? ([0] to quit)")

    #In case the input is False, continue
    while True:
        betIN = input(colorama.Fore.WHITE+"> ")
        print()
        
        #Convert betIN to integer and Value checking
        try:
            betIN = int(betIN)

            #exit point
            if betIN == 0:
                print(colorama.Fore.GREEN+"Hope to see you again, ",user +"!")
                print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
                exit()  
            
            #Allowed betting ranged from 1 to 500
            elif betIN <= betVal and betIN >= 1:
                betVal -= betIN 
                print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
                print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)
                
                print()
                #DEBUGGER print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
                game_start(betIN, betVal)
                break

            elif betIN > 500:
                print(colorama.Fore.RED+"not enough balance")
                continue

            elif betIN <= -1:
                print(colorama.Fore.RED+"not enough")
                continue

            else:
                raise ValueError

        except ValueError:
            print(colorama.Fore.RED+"INVALID. Please input a number/integer")
            print()
            continue

#Player hand actions
def Action(betIN, betVal):
    #DEBUGGER print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
    from functions import Hit_0, Stand_1, Surrender_2, Double_3, Split_4,AllIn_5
    print()
    print(colorama.Fore.GREEN+"[0] Hit")
    print("[1] Stand")
    print("[2] Surrender")
    print("[3] Double")
    print("[4] Split")
    print("[5] All in")
    print("[Q] Quit")

    #In case the input is False, continue
    while True:
        ChosenAction = input(colorama.Fore.WHITE+"> ")
        print()
        
        #exit point
        if ChosenAction == "Q" or ChosenAction == "q":
            print(colorama.Fore.GREEN+"Hope to see you again, ",user +"!")
            print("----------------------------------------------------------------------------"+colorama.Fore.RESET)
            exit()

        #Convert ChosenAction to integer and Value checking
        try:
            ChosenAction = int(ChosenAction)

            #if input is less than 0 or greater than 5, raise value error
            if ChosenAction < 0 or ChosenAction > 5:
                raise ValueError

        except ValueError:
            print(colorama.Fore.RED+">INVALID. Please only select a number from the displayed option")
            print()
            continue
        
        #Hit
        if ChosenAction == 0:
            Hit_0()
            break
        
        #Stand
        elif ChosenAction == 1:
            Stand_1(betIN, betVal)
            break
        
        #Surrender
        elif ChosenAction == 2:
            Surrender_2(betIN, betVal)
            break
        
        #Double
        elif ChosenAction == 3:
            Double_3(betIN, betVal)
            break
        
        #Split
        elif ChosenAction == 4:
            Split_4(betIN, betVal)
            break
        
        #All-in
        elif ChosenAction == 5:
            AllIn_5(betIN, betVal)
            break

        else:
            print(colorama.Fore.RED+"something went wrong")
            continue


#THINGS TO LEARN:
    #More about try exception and Error types