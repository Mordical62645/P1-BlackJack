import math
import colorama

#Card animations
card_art = {
    #Card animation Q
    "Q": [
        ".------.",
        "|Q.--. |",
        "| (\/) |",
        "| :\/: |",
        "| '--'Q|",
        "`------'"
    ],
    #Card animation K
    "K": [
        ".------.",
        "|K.--. |",
        "| :/\: |",
        "| :\/: |",
        "| '--'K|",
        "`------'"
    ],
    #Card animation J
    "J": [
        ".------.",
        "|J.--. |",
        "| :(): |",
        "| ()() |",
        "| '--'J|",
        "`------'"
    ],
    #Card animation A
    "A": [
        ".------.",
        "|A.--. |",
        "| (\/) |",
        "| :\/: |",
        "| '--'A|",
        "`------'"
    ]
}

#When called, reassign the card variable from functions.py to a string type list
def Cards_render(cards: list[str]):
    card_lines = []

    for card in cards:

        if card in card_art: #if the chosen card (from randomizer in functions.py) is in the card animation
            card_lines.append(card_art[card])

        #For numeric cards 
        elif isinstance(card, int) and card in range(1, 11):
            card_art_numeric = [
                f".------.",
                f"|{card}.--. |",
                f"| (\/) |",
                f"| :\/: |",
                f"| '--'{card}|",
                f"`------'",
            ]
            card_lines.append(card_art_numeric)

        else:
            print(colorama.Fore.RED)
            print("Invalid cards provided.")
            print(colorama.Fore.RESET)

    result = "\n".join("".join(lines) for lines in zip(*card_lines))
    return result 

#Card container to show
Dealer = []
Player = []

#Progress bar/loading
def run_progress_bar(): #call this function outside the script

    def progress_bar(progress, total): #call this function within the script
        percent = 100 * (progress / float(total))

        #alt+219 for a block code text
        #
        bar = "█" * int(percent) + "-" * (100 - int(percent))
    
        if percent >= 0 and percent <= 19:
            print(colorama.Fore.RED + f"\r|{bar}| {percent:.2f}%", end="\r")
        
        elif percent >= 20 and percent <= 79:
            print(colorama.Fore.YELLOW + f"\r|{bar}| {percent:.2f}%", end="\r")
        
        elif percent >= 80 and percent <= 100:
            print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")

    numbers = [x * 5 for x in range (2000, 3000)]
    results = []
    progress_bar(0, len(numbers))

    for i, x in enumerate(numbers):
        results.append(math.factorial(x))
        progress_bar(i + 1, len(numbers))
    
    print(colorama.Fore.RESET)
    
#For introductory title screen
def title_card():

    #ASCII: Big Money-ne(north-east) 
    #https://patorjk.com/software/taag/?fbclid=IwAR3SvS1O9C4zUzIjW6SzLleDp0wDaFOIYDIV1ooMTafChEic34pPjRX-L1M#p=display&h=1&f=Big%20Money-ne&t=Stackulator
    print(colorama.Fore.YELLOW)
    print(" /$$$$$$$  /$$                     /$$          /$$$$$                     /$$      ")
    print("| $$__  $$| $$                    | $$         |__  $$                    | $$      ")
    print("| $$  \ $$| $$  /$$$$$$   /$$$$$$$| $$   /$$      | $$  /$$$$$$   /$$$$$$$| $$   /$$")
    print("| $$$$$$$ | $$ |____  $$ /$$_____/| $$  /$$/      | $$ |____  $$ /$$_____/| $$  /$$/")
    print("| $$__  $$| $$  /$$$$$$$| $$      | $$$$$$/  /$$  | $$  /$$$$$$$| $$      | $$$$$$/ ")
    print("| $$  \ $$| $$ /$$__  $$| $$      | $$_  $$ | $$  | $$ /$$__  $$| $$      | $$_  $$ ")
    print("| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$")
    print("|_______/ |__/ \_______/ \_______/|__/  \__/ \______/  \_______/ \_______/|__/  \__/")
    print("- Made by Marco Tecson")
    print(colorama.Fore.RESET) 
    print()

#THINGS TO LEARN:
    #import math
        #factorial
    #cards: list[str]
    #.append()
    #.isinstance()
    #result = "\n".join("".join(lines) for lines in zip(*card_lines))
        #.join()
    #zip()
    #enumerate()
    #.factorial()
    #len()
    #in range()

    #Learn how progress bar works

