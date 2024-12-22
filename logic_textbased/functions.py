import random #Card shuffling involves randomizing of cards in improbable way.
import colorama #Font color

def info(): 
    from inputs import first_option
    print()
    print(colorama.Fore.GREEN+"Let's play BlackJack!")
    print("Rules: Beat the Dealer!")
    print("Win: Closer to 21 than the dealer without getting over 21 | Pay: Same value to bet 1:1")
    print("Lose: Dealer is closer to 21 than you or go over 21")
    print("Same value to the dealer = Push (nor win nor lose retry)")
    print()
    print(colorama.Fore.LIGHTYELLOW_EX+"Made by Marco Tecson")
    print(colorama.Fore.GREEN+"BlackJack v.1.0.0")
    print("Made with Python")
    print()
    first_option() #return to main menu

#Add another stack to the user/player's hand
def Hit_0(): 
    from inputs import Action, user, betIN, betVal
    from render import Cards_render, Player
    print(colorama.Fore.GREEN+"You chose to hit!")
    print()

    playerhand = []

    playerhand.append(Playerval1)
    playerhand.append(Playerval2)

    PlayrandomOnHit = deck[0]
    deck.pop(0)

    playerhand.append(PlayrandomOnHit)

    Player.extend([Playerval1, Playerval2, PlayrandomOnHit])
    print(colorama.Fore.WHITE+Cards_render(Player))
    print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}] [{PlayrandomOnHit}]")


    Action(betIN, betVal)



#Win or Lose logic
def commit_win_or_lose(betIN, betVal): 
    from inputs import re_bet, lose_options

    dealer_pick_card(dealrandom1)
    
    #Player lose
    if DealerSum > PlayerSum and DealerSum <= 21:
        print (colorama.Fore.GREEN+"BUST!")
        print()

        betIN *= 0
            
        print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
        print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)

        if betVal == 0:
            print()
            print(colorama.Fore.RED+"Sorry, you don't have enough balance to play another round")
            print(colorama.Fore.GREEN+"Do you wish to restart the game again?")
            lose_options()

        else:
            print ("----------------------------------------------------------------------------")

            re_bet(betIN, betVal)
        
    #Player win
    elif PlayerSum > DealerSum and PlayerSum <= 21:
        print (colorama.Fore.GREEN+"BLACKJACK!")
        print()

        betIN *= 2
        betVal += betIN
        betIN *= 0

        print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
        print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)

        print ("----------------------------------------------------------------------------")
        
        re_bet(betIN, betVal)

    #Tie
    elif PlayerSum == DealerSum:
        print (colorama.Fore.GREEN+"PUSH!")
        print()

        betVal += betIN
        betIN *= 0

        print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
        print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)

        print ("----------------------------------------------------------------------------")

        re_bet(betIN, betVal)

#Stand
def Stand_1(betIN, betVal):
    print("You chose to stand!")
    commit_win_or_lose(betIN, betVal)

#Surrender
def Surrender_2(betIN, betVal):
    #print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
    from inputs import re_bet
    print(colorama.Fore.GREEN+"You chose to surrender. Lose half of the bet.")
    print()

    dealer_pick_card(dealrandom1)
    print()

    #print(colorama.Fore.BLUE+f"IGNORE. betVal: {betVal} betIN: {betIN}")
    betIN /= 2
    betVal += betIN
    betIN *= 0

    print(colorama.Fore.GREEN+"Bet: "+colorama.Fore.WHITE+f"{betIN}")
    print(colorama.Fore.GREEN+"Balance: "+colorama.Fore.WHITE+f"{betVal}"+colorama.Fore.GREEN)

    print ("----------------------------------------------------------------------------")
        
    re_bet(betIN, betVal)
        
#Double
def Double_3(betIN, betVal):
    from inputs import Action
    print(colorama.Fore.GREEN+"Double the bet!")
    print()

    try_betVal = betVal - betIN

    if try_betVal < 0 :
        print(colorama.Fore.RED+"Sorry, not enough balance")
        Action(betIN, betVal)

    else:
        betVal -= betIN  
        betIN *= 2
        print(colorama.Fore.GREEN+"The bet is now "+colorama.Fore.WHITE+f"{betIN}")
        print("Balance: "+colorama.Fore.WHITE+f"{betVal}")
        commit_win_or_lose(betIN, betVal)

#Split
def Split_4(betIN, betVal):
    pass

#All-in
def AllIn_5(betIN, betVal):
    from inputs import Action
    if betVal == 0:
        print(colorama.Fore.RED + "Sorry, not enough balance")
        Action(betIN, betVal)
        
    else:
        print(colorama.Fore.GREEN + "All in!")
        betIN += betVal
        betVal -= betVal
        print()
        print(colorama.Fore.GREEN + "The bet is now " + colorama.Fore.WHITE + f"{betIN}")
        print("Balance: " + colorama.Fore.WHITE + f"{betVal}")
        commit_win_or_lose(betIN, betVal)

def cards_state():
    Hearts = list(range(2, 11)) + ["J", "Q", "K", "A"]
    Spades = list(range(2, 11)) + ["J", "Q", "K", "A"]
    Clubs = list(range(2, 11)) + ["J", "Q", "K", "A"]
    Diamonds = list(range(2, 11)) + ["J", "Q", "K", "A"]
    
    Card_values = {"J": 10, "Q": 10, "K": 10}

    global deck
    deck = Hearts + Spades + Clubs + Diamonds
    random.shuffle(deck)

    return deck, Card_values

#Dealer hand
def dealer_pick_card(dealrandom1):
    from render import Cards_render, Dealer
    global Dealerval1
    global DealerSum

    deck, Card_values = cards_state()

    dealrandom2 = deck[0]

    if dealrandom1 in Card_values and dealrandom2 not in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 1") 
        Dealerval1 = dealrandom1

        if dealrandom2 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 2") 
            Dealerval2 = "A"
            Dealer.extend([Dealerval1, Dealerval2])

            if Card_values[dealrandom1] + 11 <= 21:
                Dealerval2 = 11

            else:
                Dealerval2 = 1

        else:
            #print(colorama.Fore.BLUE+"IGNORE. Point 3") 
            Dealerval2 = dealrandom2
            Dealer.extend([Dealerval1, Dealerval2])
        
        print(colorama.Fore.WHITE+Cards_render(Dealer))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}] [{dealrandom2}]")
            
        DealerSum = Card_values[Dealerval1] + Dealerval2
        print()

    elif dealrandom2 in Card_values and dealrandom1 not in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 3") 
        Dealerval2 = dealrandom2

        if dealrandom1 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 4") 
            Dealerval1 = "A"
            Dealer.extend([Dealerval1, Dealerval2])

            if Card_values[dealrandom2] + 11 <= 21:
                Dealerval1 = 11

            else:
                Dealerval1 = 1

        else:
            Dealerval1 = dealrandom1
            Dealer.extend([Dealerval1, Dealerval2])

        print(colorama.Fore.WHITE+Cards_render(Dealer))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}] [{dealrandom2}]")

        DealerSum = Dealerval1 + Card_values[Dealerval2]
        print()

    elif dealrandom1 in Card_values and dealrandom2 in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 5") 
        Dealerval1 = dealrandom1
        Dealerval2 = dealrandom2

        Dealer.extend([Dealerval1, Dealerval2])
        print(colorama.Fore.WHITE+Cards_render(Dealer))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}] [{dealrandom2}]")

        DealerSum = Card_values[Dealerval1] + Card_values[Dealerval2]
        print()
    
    elif dealrandom2 == "A" and dealrandom1 == "A":
        #print(colorama.Fore.BLUE+"IGNORE. Point 6") 
        Dealerval1 = "A"
        Dealerval2 = "A"
        Dealer.extend([Dealerval1, Dealerval2])

        Dealerval2 = 11
        Dealerval1 = 1

        print(colorama.Fore.WHITE+Cards_render(Dealer))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}] [{dealrandom2}]")

        DealerSum = Dealerval1 + Dealerval2
        print()
        
    else:
        #print(colorama.Fore.BLUE+"IGNORE. Point 7") 
        Dealerval1 = None
        Dealerval2 = None

        if dealrandom1 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 8") 
            Dealerval1 = "A"
            Dealerval2 = dealrandom2
            Dealer.extend([Dealerval1, Dealerval2])

            if dealrandom2 + 11 <= 21:
                Dealerval1 = 11

            else:
                Dealerval1 = 1
        
        elif dealrandom2 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 9") 
            Dealerval2 = "A"
            Dealerval1 = dealrandom1
            Dealer.extend([Dealerval1, Dealerval2])

            if dealrandom1 + 11 <= 21:
                Dealerval2 = 11

            else:
                Dealerval2 = 1

        else:
           #print(colorama.Fore.BLUE+"IGNORE. Point 10") 
            Dealerval1 = dealrandom1
            Dealerval2 = dealrandom2
            Dealer.extend([Dealerval1, Dealerval2])
        
        print(colorama.Fore.WHITE+Cards_render(Dealer))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}] [{dealrandom2}]")

        DealerSum = Dealerval1 + Dealerval2
        print()
    
    deck.pop(0)

def game_start(betIN, betVal):
    from render import Cards_render, Player, Dealer
    from inputs import Action, user

    #restart
    Dealer.clear()
    Player.clear()

    global DealerSum, Dealerval1, dealrandom1
    global PlayerSum, Playerval1, Playrandom1, Playrandom2, Playerval2

    deck, Card_values = cards_state()

    dealrandom1 = deck[0]

    if dealrandom1 in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 11") 
        Dealerval1 = dealrandom1

        print(colorama.Fore.WHITE+Cards_render([Dealerval1]))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}]")
        print()
    
    elif dealrandom1 == "A":
        #print(colorama.Fore.BLUE+"IGNORE. Point 12") 
        Dealerval1 = "A"

        print(colorama.Fore.WHITE+Cards_render([Dealerval1]))
        deal_A = "A"
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{deal_A}]")
        print()
    
    else:
        #print(colorama.Fore.BLUE+"IGNORE. Point 13") 
        Dealerval1 = dealrandom1

        print(colorama.Fore.GREEN) 
        print(colorama.Fore.WHITE+Cards_render([Dealerval1]))
        print(colorama.Fore.GREEN+f"Dealer: "+colorama.Fore.WHITE+f"[{dealrandom1}]")
        print()

    print(colorama.Fore.GREEN+"Dealer gives you a card!")
    print()

    deck.pop(0)


    Playrandom1 = deck[0]
    deck.pop(0)

    Playrandom2 = deck[0]
    deck.pop(0)


    if Playrandom1 in Card_values and Playrandom2 not in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 14") 
        Playerval1 = Playrandom1

        if Playrandom2 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 15") 
            Playerval2 = "A"
            Player.extend([Playerval1, Playerval2])

            if Card_values[Playrandom1] + 11 <= 21:
                Playerval2 = 11

            else:
                Playerval2 = 1

        else:
            #print(colorama.Fore.BLUE+"IGNORE. Point 16") 
            Playerval2 = Playrandom2
            Player.extend([Playerval1, Playerval2])
        
        print(colorama.Fore.WHITE+Cards_render(Player))
        print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}]")

        PlayerSum = Card_values[Playerval1] + Playerval2
        Action(betIN, betVal)

    elif Playrandom2 in Card_values and Playrandom1 not in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 16") 
        Playerval2 = Playrandom2

        if Playrandom1 == "A":
            #print(colorama.Fore.BLUE+"IGNORE. Point 17") 
            Playerval1 = "A"
            Player.extend([Playerval1, Playerval2])

            if Card_values[Playrandom2] + 11 <= 21:
                Playerval1 = 11

            else:
                Playerval1 = 1

        else:
            #print(colorama.Fore.BLUE+"IGNORE. Point 18") 
            Playerval1 = Playrandom1
            Player.extend([Playerval1, Playerval2])

        print(colorama.Fore.WHITE+Cards_render(Player))
        print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}]")

        PlayerSum = Playerval1 + Card_values[Playerval2]
        Action(betIN, betVal)
    
    elif Playrandom1 in Card_values and Playrandom2 in Card_values:
        #print(colorama.Fore.BLUE+"IGNORE. Point 19") 
        Playerval1 = Playrandom1
        Playerval2 = Playrandom2

        Player.extend([Playerval1, Playerval2])
        print(colorama.Fore.WHITE+Cards_render(Player))
        print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}]")

        PlayerSum = Card_values[Playerval1] + Card_values[Playerval2]
        Action(betIN, betVal)

    elif Playrandom2 == "A" and Playrandom1 == "A":
        #print(colorama.Fore.BLUE+"IGNORE. Point 20") 
        Playerval1 = "A"
        Playerval2 = "A"
        Player.extend([Playerval1, Playerval2])

        Playerval2 = 11
        Playerval1 = 1

        print(colorama.Fore.WHITE+Cards_render(Player))
        print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}]")

        PlayerSum = Playerval1 + Playerval2
        Action(betIN, betVal)

    else:
        Playerval1 = None
        Playerval2 = None
        #print(colorama.Fore.BLUE+"IGNORE. Point 21") 
        
        if Playrandom1 == "A":
            print(colorama.Fore.BLUE+"IGNORE. Point 22")
            Playerval1 = "A"
            Playerval2 = Playrandom2
            Player.extend([Playerval1, Playerval2])

            if Playrandom2 + 11 <= 21:
                Playerval1 = 11

            else:
                Playerval1 = 1

        elif Playrandom2 == "A":
           #print(colorama.Fore.BLUE+"IGNORE. Point 23")
            Playerval2 = "A"
            Playerval1 = Playrandom1
            Player.extend([Playerval1, Playerval2])

            if Playrandom1 + 11 <= 21:
                Playerval2 = 11

            else:
                Playerval2 = 1

        else:
            #print(colorama.Fore.BLUE+"IGNORE. Point 24")
            Playerval1 = Playrandom1
            Playerval2 = Playrandom2
            Player.extend([Playerval1, Playerval2])
        
        print(colorama.Fore.WHITE+Cards_render(Player))
        print(colorama.Fore.WHITE+f"{user}: [{Playrandom1}] [{Playrandom2}]")
        
        PlayerSum = Playerval1 + Playerval2
        Action(betIN, betVal)