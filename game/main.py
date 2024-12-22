##### LIBRARIES #####
import sys
import pygame
import pygame_gui
import random

##### CARD #####
class Card:
    def __init__(self, cardvalue, cardsuit): # Card characteristics
        self.cardvalue = cardvalue # 2 < 9
        self.cardsuit = cardsuit  # hearts, spades, clubs, diamonds
        self.cardimage = None # File

    def load_image(self): # image loader
        if self.cardimage is None: 
            self.cardimage = pygame.image.load(f"graphics/Cards/{self.cardvalue}{self.cardsuit}.png") # locate image file

    def __repr__(self):
        return f"{self.cardvalue}{self.cardsuit}"
    
class Chips:
    def __init__(self, chipvalue, chipcolor): # Chips characteristics
        self.chipvalue = chipvalue # 5, 10, 50, 100, 500, 1000
        self.chipcolor = chipcolor # Gray, Red, Blue, Yellow, Black, Violet, Orange
        self.chipimage = None
    
    def load_image(self):
        if self.chipimage is None:
            self.chipimage = pygame.image.load(f"graphics/Chips/{self.chipvalue}{self.chipcolor}.png")

    def __repr__(self):
        return f"{self.chipvalue}{self.chipcolor}"

def deck_func():
    global deckvalues, deckcount
    values = list(range(2, 11)) + ["J", "Q", "K", "A"] # [2, 3, 4, 5, 6, 7, 8 , 9, 10, Jack, Queen, King, Ace] 
    suits = ['h', 's', 'c', 'd']
    facecard_values = {"J": 10, "Q": 10, "K": 10, "A":11} # [Jack, Queen, King, = 10, Ace = 11]
    deck = [Card(value, suit) for suit in suits for value in values] # [2h, 3h, 4h, 5h, 6h, 7h, 8h, 9h, 10h, Jh, Qh, Kh, Ah...]
    random.shuffle(deck) # Deck suffle
    deckcount = len(deck) # current number of deck (52)
    deckvalues = [facecard_values.get(str(card.cardvalue), card.cardvalue)for card in deck] # We'll get the value of facecards and default values only
    print(f"Deck: {deck}")
    print(f"Stack: {deckcount}")
    return deck

def dealer_dealing_cards(dealertotal, playertotal):
    captured_game_state = screen.copy()
    screen.blit(captured_game_state, (0, 0))
    captured_image = screen.copy()

    blind_card_posx = 10
    blind_card_posy = 10
    
    blind_card_targetx = 350
    blind_card_targety = 50

    frames = 30
    
    if dealertotal <= 16:

        while dealertotal <= 16:
            channel1.play(sound1)

            global deckcount
            deckcount -= 1
            
            captured_image = screen.copy()
            dealer_card = deck.pop()
            dealerscore.append(deckvalues.pop())
            dealer_hand.append(dealer_card)
            
            dealertotal = sum(dealerscore)

            global dealer_card_targetx
            dealer_card_targetx += 100

            for frame in range(frames):
                    
                # Calculate intermediate position
                progress = frame / frames
                blind_card_intermediate_x = blind_card_posx + (blind_card_targetx - blind_card_posx) * progress
                blind_card_intermediate_y = blind_card_posy + (blind_card_targety - blind_card_posy) * progress

                # Draw all elements
                screen.blit(captured_image, (0, 0))            
                
                for _, card in enumerate(dealer_hand):
                    card.load_image() 
                    screen.blit(card.cardimage, (blind_card_intermediate_x, blind_card_intermediate_y))

                channel2.play(sound2)
                
                pygame.display.update()
                pygame.time.delay(10)
            
            blind_card_targetx += 100

            print()
            print(f"Deck: {deck}")
            print(f"Deck values: {deckvalues}")
            print(f"Stack: {deckcount}")
            print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
            print(f"Player's hand: {player_hand} Score: {playertotal}")

    pygame.time.delay(1000)

    if len(dealer_hand) == 2 :
        channel2.play(sound2) 

    return dealertotal, playertotal
    
def deal_initial_cards(deck):
    global player_hand, playertotal, playerscore, dealerscore, dealer_hand, dealertotal, deckvalues, deckcount
    player_hand = []
    playerscore = []

    dealer_hand = []
    dealerscore = []
    
    for _ in range(2):
        player_card = deck.pop()
        playerscore.append(deckvalues.pop())
        player_hand.append(player_card)
        deckcount -= 1

        dealer_card = deck.pop()
        dealerscore.append(deckvalues.pop())
        dealer_hand.append(dealer_card)
        deckcount -= 1

    playertotal = sum(playerscore) 
    dealertotal = sum(dealerscore) 

##### ACTION FUNCTIONS #####
def Hit_func(dealertotal, playertotal):
    global captured_image
    captured_image = screen.copy()

    player_card = deck.pop()
    playerscore.append(deckvalues.pop())
    player_hand.append(player_card)
    
    playertotal = sum(playerscore)
    dealertotal = sum(dealerscore)

    global deckcount
    deckcount -= 1

    channel1.play(sound1)

    global hit_targetx, hit_targety
    hit_card_posx, hit_card_posy = 10, 10 
    hit_targetx += 100  
    hit_targety = 250 

    global x, y
    x = 300
    y = 185

    card_load_posx = 250
    card_load_posy = 50
    
    frames = 30  
    for frame in range(frames):
            
        # Calculate intermediate position
        global intermediate_x, intermediate_y
        intermediate_x = hit_card_posx + (hit_targetx - hit_card_posx) * (frame / frames)
        intermediate_y = hit_card_posy + (hit_targety - hit_card_posy) * (frame / frames)

        # Draw all elements
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        screen.blit(captured_image, (0, 0))
        screen.blit(blind_card, (intermediate_x, intermediate_y))
        channel2.play(sound2)
        
        pygame.display.update()
        pygame.time.delay(10)

    print()
    print(f"Deck: {deck}")
    print(f"Deck values: {deckvalues}")
    print(f"Stack: {deckcount}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    if playertotal > 21:        
        print("BUST!")
        for _, card in enumerate(dealer_hand):
            card.load_image() 
            screen.blit(card.cardimage, (card_load_posx, card_load_posy))
        
        for _, card in enumerate(player_hand):
            card.load_image() 
            screen.blit(card.cardimage, (intermediate_x, intermediate_y))
            
            global captured_game_state
            captured_game_state = screen.copy() 
            
        titlecard_surface = titlecard.render("BUST!", False, "Black")
        screen.blit(titlecard_surface, (x, y))

        pygame.display.update()
        pygame.time.delay(1000)
        
        dealer_dealing_cards(dealertotal, playertotal)
        main()

def Stand_func(dealertotal, playertotal):    
    titlecard = pygame.font.Font("font/KarenFat.ttf", 50)
    
    x = 300
    y = 185

    card_load_posx = 250
    card_load_posy = 50
    
    specific_card_index = 1  
    specific_card = dealer_hand[specific_card_index]
    specific_card.load_image()
    screen.blit(specific_card.cardimage, (card_load_posx, card_load_posy)) 

    dealer_dealing_cards(dealertotal, playertotal)

    playertotal = sum(playerscore)
    dealertotal = sum(dealerscore)

    print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    # WIN CONDITION
    if (playertotal <= 21 and (dealertotal > 21 or playertotal > dealertotal)):
        # Player wins if they have a higher score than the dealer
        print("WIN!")
        titlecard_surface = titlecard.render("WIN!", False, "Black") 
        screen.blit(titlecard_surface, (x, y))
        pygame.display.update()  

    # LOSE CONDITION 
    elif (playertotal > 21 or (dealertotal <= 21 and dealertotal > playertotal)):
        # Dealer wins if player busts or dealer has a higher score
        print("BUST!")
        titlecard_surface = titlecard.render("BUST!", False, "Black") 
        screen.blit(titlecard_surface, (x, y))
        pygame.display.update()

    # PUSH CONDITION
    elif playertotal == dealertotal:
        print("PUSH!")
        titlecard_surface = titlecard.render("PUSH!", False, "Black") 
        screen.blit(titlecard_surface, (x, y))
        pygame.display.update()  

    pygame.time.delay(1000)
    main()

def Surrender_func(dealertotal, playertotal):
    titlecard = pygame.font.Font("font/KarenFat.ttf", 50)
    
    x = 250
    y = 185

    card_load_posx = 250
    card_load_posy = 50
    
    specific_card_index = 1 
    specific_card = dealer_hand[specific_card_index]
    specific_card.load_image()
    screen.blit(specific_card.cardimage, (card_load_posx, card_load_posy))  

    dealer_dealing_cards(dealertotal, playertotal)

    playertotal = sum(playerscore)
    dealertotal = sum(dealerscore)

    print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    print("SURRENDER!")
    titlecard_surface = titlecard.render("SURRENDERED!", False, "Black") 
    screen.blit(titlecard_surface, (x, y))
    pygame.display.update()
                    
    pygame.time.delay(1000)
    main()

def Double_func():
    pass

def Split_func():
    pass

##### ANIMATION FUNCTIONS #####
def first_deal_anim():
    # Create a new temporary screen for the animation
    screen.blit(ground, (0, 0))
    screen.blit(card_deck, (10, 10))

    global drawing, sound1, channel1
    drawing = "audio/sfx/drawing.mp3"
    sound1 = pygame.mixer.Sound(drawing)
    channel1 = pygame.mixer.Channel(0)
    channel1.set_volume(10)  # Set the volume to 50%
    
    global blind_card
    blind_card = pygame.image.load(f"graphics/Card_Back/blind_card.png")

    # Define initial positions and target positions for animations
    blind_card_posx = 10
    blind_card_posy = 10
    blind_card_targetx = [150, 250, 250, 150]
    blind_card_targety = [250, 50, 250, 50]

    frames = 30
    
    for i in range(len(blind_card_targetx)):
        channel1.play(sound1)
        captured_image = screen.copy()  

        for frame in range(frames):
            # Calculate the intermediate positions with smoother transition
            progress = frame / frames
            blind_card_intermediate_x = blind_card_posx + (blind_card_targetx[i] - blind_card_posx) * progress
            blind_card_intermediate_y = blind_card_posy + (blind_card_targety[i] - blind_card_posy) * progress

            screen.blit(captured_image, (0, 0))  # Blit the captured image
            screen.blit(blind_card, (blind_card_intermediate_x, blind_card_intermediate_y))
            
            pygame.display.update()
            pygame.time.delay(10) 
    
    print(f"{blind_card_targetx}:{blind_card_targety}")

##### BETTING #####
def bet_start():
    chips_dict = {
        'Gray': 1,
        'Red': 5,
        'Blue': 10,
        'Yellow': 50,
        'Black': 100,
        'Violet': 500,
        'Orange': 1000
    }    
    bet = 0
    
    global action_manager
    action_manager = pygame_gui.UIManager((800, 480))
    
    # Create buttons
    bet_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 400), (50, 50)), text='1', manager=action_manager)
    bet_5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (50, 50)), text='5', manager=action_manager)
    bet_10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (50, 50)), text='10', manager=action_manager)
    bet_50 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 400), (50, 50)), text='50', manager=action_manager)
    bet_100 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 400), (50, 50)), text='100', manager=action_manager)
    bet_500 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 400), (50, 50)), text='500', manager=action_manager)
    bet_1000 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 400), (50, 50)), text='1000', manager=action_manager)
    
    while True:
        # Fill screen with background
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        
        # Render chips
        x = 60
        for color, value in chips_dict.items():
            chip = Chips(value, color)
            chip.load_image()
            if isinstance(chip.chipimage, pygame.Surface): 
                screen.blit(chip.chipimage, (x, 300))
                x += 100

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == bet_1:
                        # Perform action
                        bet += 1
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_5:
                        # Perform action
                        bet += 5
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_10:
                        # Perform action
                        bet += 10
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_50:
                        # Perform action
                        bet += 50
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_100:
                        # Perform action
                        bet += 100
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_500:
                        # Perform action
                        bet += 500
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_1000:
                        # Perform action
                        bet += 1000
                        print(f"Bet: {bet}")
                
            # Update manager with the event
            action_manager.process_events(event)

        # Update the UI
        action_manager.update(1 / 60)  # Assuming a 60 FPS game loop
        
        # Draw the UI
        action_manager.draw_ui(screen)
        
        # Update display and control frame rate
        pygame.display.update()
        fps.tick(60)
        
##### PLAY #####
def game_start():
    print(f"Deck: {deck}")
    print(f"Deck values: {deckvalues}")
    print(f"Stack: {deckcount}")
    print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    global dealing, sound2, channel2
    dealing = "audio/sfx/dealing.mp3"
    sound2 = pygame.mixer.Sound(dealing)
    channel2 = pygame.mixer.Channel(1)
    channel2.set_volume(0.5)  # Set the volume to 50%
    channel2.play(sound2)
    
    global action_manager
    action_manager = pygame_gui.UIManager((800, 480))

    # Create buttons
    global hit_button, stand_button, surrender_button, double_button, split_button
    hit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (100, 50)), text='Hit', manager=action_manager)
    stand_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (100, 50)), text='Stand', manager=action_manager)
    surrender_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)), text='Surrender', manager=action_manager)
    double_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 400), (100, 50)), text='Double', manager=action_manager)
    split_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 400), (100, 50)), text='Split', manager=action_manager)
                            
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == hit_button:
                        print("Hit button pressed")
                        Hit_func(dealertotal, playertotal)

                    elif event.ui_element == stand_button:
                        print("Stand button pressed")
                        Stand_func(dealertotal, playertotal)

                    elif event.ui_element == surrender_button:
                        print("Surrender button pressed")
                        Surrender_func(dealertotal, playertotal)

                    elif event.ui_element == double_button:
                        print("Double button pressed")
                        Double_func()

                    elif event.ui_element == split_button:
                        print("Split button pressed")
                        Split_func()

            action_manager.process_events(event)
        
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        
        
        # Display player's cards
        for i, card in enumerate(player_hand):
            card.load_image()  # Load the image if not loaded
            screen.blit(card.cardimage, (50 + i * 100 + 100, 250))  # Adjust position as needed        

        # Display dealer's cards
        for i, card in enumerate(dealer_hand):
            card.load_image()    
            screen.blit(card.cardimage, (50 + i * 100 + 100, 50))  # Adjust position as needed

            if i == 1:
                screen.blit(blind_card, (250, 50))
        
        #BLACKJACK INSTANT WIN
        #if (playertotal == 21 and len(player_hand) == 2 and dealertotal != 21):  # Blackjack!
            #print("BLACKJACK!")
            #titlecard_surface = titlecard.render("BLACKJACK!", False, "Black") 
            #resolution.blit(titlecard_surface, (x, y))
            #pygame.display.update()  

        # Update everything
        action_manager.update(1 / 60.0)
        action_manager.draw_ui(screen)

        pygame.display.update()
              
##### MAIN #####
def main():
    global hit_targetx, dealer_card_targetx
    hit_targetx = 250
    dealer_card_targetx = 250
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("BlackJack")

    # Initialize music
    pygame.mixer.music.load("audio/bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    # Create screen
    global screen
    screen = pygame.display.set_mode((800, 480))
    screen.fill('Green')

    global fps, titlecard
    fps = pygame.time.Clock()
    titlecard = pygame.font.Font("font/KarenFat.ttf", 50)

    # Surface
    global ground, titlecard_surface
    ground = pygame.image.load("graphics/ground.jpg")
    titlecard_surface = titlecard.render("BlackJack", False, "Black")

    # Card Deck
    global card_deck
    card_deck = pygame.image.load("graphics/Card_Deck/card_deck.png")

    # Initialize pygame_gui
    global menu_manager
    menu_manager = pygame_gui.UIManager((800, 480))
    
    # Initialize game state
    global deck
    deck = deck_func()
    deal_initial_cards(deck)

    print(f"Deck: {deck}")
    print(f"Stack: {deckcount}")

    # Create buttons
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (100, 50)), text='Play', manager=menu_manager)
    info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (100, 50)), text='Info', manager=menu_manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)), text='Quit', manager=menu_manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == play_button:
                        print("Play button pressed")
                        bet_start()
                        first_deal_anim()
                        game_start()

                    elif event.ui_element == info_button:
                        print("Info button pressed")

                    elif event.ui_element == quit_button:
                        pygame.quit()
                        exit()

            menu_manager.process_events(event)

        # Draw all elements
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        screen.blit(titlecard_surface, (360, 185))
            
        # Update everything
        menu_manager.update(1 / 60.0)
        menu_manager.draw_ui(screen)

        pygame.display.update()
        fps.tick(60)

if __name__ == "__main__":
    main()