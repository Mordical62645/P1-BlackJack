# ~!CARD TEST!~
# Things to achieve:
# 1. Specific card count 
# 2. A deck
# 3. Shuffling (Randomize)
# 4. Subtrack cards
# 5. Reshuffle if all cards are used
# Data Structure: Stack

import random

# 1. Specific card count 
Hearts = [f"{i}h" for i in range(2, 11)] + ["Jh", "Qh", "Kh", "Ah"]
Spades = [f"{i}s" for i in range(2, 11)] + ["Js", "Qs", "Ks", "As"]
Clubs = [f"{i}c" for i in range(2, 11)] + ["Jc", "Qc", "Kc", "Ac"]
Diamonds = [f"{i}d" for i in range(2, 11)] + ["Jd", "Qd", "Kd", "Ad"]

Card_values = {"J": 10, "Q": 10, "K": 10}

# 2. A deck
deck = Hearts + Spades + Clubs + Diamonds

# 3. Shuffling (Randomize)
random.shuffle(deck)
print(deck)

while True:
    pick_button = input("> ")

    if pick_button == '0':

        # 6. Reshuffle if all cards are used
        if not deck:
            Hearts = [f"{i}h" for i in range(2, 11)] + ["Jh", "Qh", "Kh", "Ah"]
            Spades = [f"{i}s" for i in range(2, 11)] + ["Js", "Qs", "Ks", "As"]
            Clubs = [f"{i}c" for i in range(2, 11)] + ["Jc", "Qc", "Kc", "Ac"]
            Diamonds = [f"{i}d" for i in range(2, 11)] + ["Jd", "Qd", "Kd", "Ad"]

            Card_values = {"J": 10, "Q": 10, "K": 10}
            deck = Hearts + Spades + Clubs + Diamonds
            random.shuffle(deck)
            print(deck)
        
        pick = deck[0]
        print(pick)

        # 5. Subtract cards
        if pick in Hearts:
            Hearts.remove(pick)
            print(f"Hearts: {Hearts}")

        elif pick in Spades:
            Spades.remove(pick)
            print(f"Spades: {Spades}")

        elif pick in Clubs:
            Clubs.remove(pick)
            print(f"Clubs: {Clubs}")

        elif pick in Diamonds:
            Diamonds.remove(pick)
            print(f"Diamonds: {Diamonds}")

        deck.pop(0)
        print(f"Deck: {deck}")

        
