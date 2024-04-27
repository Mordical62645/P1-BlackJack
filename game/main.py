##### LIBRARIES #####
import sys
import pygame
import pygame_gui
import random

##### CARD #####
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = None 

    def load_image(self):
        if self.image is None:
            self.image = pygame.image.load(f"graphics/Cards/{self.value}{self.suit}.png")

    def __repr__(self):
        return f"{self.value}{self.suit}"

def deck_func():
    global deckvalues, deckcount
    suits = ['h', 's', 'c', 'd']
    values = list(range(2, 11)) + ["J", "Q", "K", "A"]
    Card_values = {"J": 10, "Q": 10, "K": 10, "A":11}
    deck = [Card(suit, value) for suit in suits for value in values]
    random.shuffle(deck)
    deckcount = len(deck)
    deckvalues = [Card_values.get(str(card.value), card.value)for card in deck]
    print(f"Deck: {deck}")
    print(f"Stack: {deckcount}")
    return deck

def dealer_dealing_cards(dealertotal, playertotal):
    captured_game_state = resolution.copy()
    resolution.blit(captured_game_state, (0, 0))
    captured_image = resolution.copy()

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
            
            captured_image = resolution.copy()
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
                resolution.blit(captured_image, (0, 0))            
                
                for _, card in enumerate(dealer_hand):
                    card.load_image() 
                    resolution.blit(card.image, (blind_card_intermediate_x, blind_card_intermediate_y))

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
    captured_image = resolution.copy()

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
        resolution.blit(ground, (0, 0))
        resolution.blit(card_deck, (10, 10))
        resolution.blit(captured_image, (0, 0))
        resolution.blit(blind_card, (intermediate_x, intermediate_y))
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
            resolution.blit(card.image, (card_load_posx, card_load_posy))
        
        for _, card in enumerate(player_hand):
            card.load_image() 
            resolution.blit(card.image, (intermediate_x, intermediate_y))
            
            global captured_game_state
            captured_game_state = resolution.copy() 
            
        titlecard_surface = titlecard.render("BUST!", False, "Black")
        resolution.blit(titlecard_surface, (x, y))

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
    resolution.blit(specific_card.image, (card_load_posx, card_load_posy)) 

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
        resolution.blit(titlecard_surface, (x, y))
        pygame.display.update()  

    # LOSE CONDITION 
    elif (playertotal > 21 or (dealertotal <= 21 and dealertotal > playertotal)):
        # Dealer wins if player busts or dealer has a higher score
        print("BUST!")
        titlecard_surface = titlecard.render("BUST!", False, "Black") 
        resolution.blit(titlecard_surface, (x, y))
        pygame.display.update()

    # PUSH CONDITION
    elif playertotal == dealertotal:
        print("PUSH!")
        titlecard_surface = titlecard.render("PUSH!", False, "Black") 
        resolution.blit(titlecard_surface, (x, y))
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
    resolution.blit(specific_card.image, (card_load_posx, card_load_posy))  

    dealer_dealing_cards(dealertotal, playertotal)

    playertotal = sum(playerscore)
    dealertotal = sum(dealerscore)

    print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    print("SURRENDER!")
    titlecard_surface = titlecard.render("SURRENDERED!", False, "Black") 
    resolution.blit(titlecard_surface, (x, y))
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
    resolution.blit(ground, (0, 0))
    resolution.blit(card_deck, (10, 10))

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
        captured_image = resolution.copy()  

        for frame in range(frames):
            # Calculate the intermediate positions with smoother transition
            progress = frame / frames
            blind_card_intermediate_x = blind_card_posx + (blind_card_targetx[i] - blind_card_posx) * progress
            blind_card_intermediate_y = blind_card_posy + (blind_card_targety[i] - blind_card_posy) * progress

            resolution.blit(captured_image, (0, 0))  # Blit the captured image
            resolution.blit(blind_card, (blind_card_intermediate_x, blind_card_intermediate_y))
            
            pygame.display.update()
            pygame.time.delay(10) 
    
    print(f"{blind_card_targetx}:{blind_card_targety}")
        
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
        
        resolution.blit(ground, (0, 0))
        resolution.blit(card_deck, (10, 10))
        
        
        # Display player's cards
        for i, card in enumerate(player_hand):
            card.load_image()  # Load the image if not loaded
            resolution.blit(card.image, (50 + i * 100 + 100, 250))  # Adjust position as needed        

        # Display dealer's cards
        for i, card in enumerate(dealer_hand):
            card.load_image()    
            resolution.blit(card.image, (50 + i * 100 + 100, 50))  # Adjust position as needed

            if i == 1:
                resolution.blit(blind_card, (250, 50))
        
        #BLACKJACK INSTANT WIN
        #if (playertotal == 21 and len(player_hand) == 2 and dealertotal != 21):  # Blackjack!
            #print("BLACKJACK!")
            #titlecard_surface = titlecard.render("BLACKJACK!", False, "Black") 
            #resolution.blit(titlecard_surface, (x, y))
            #pygame.display.update()  

        # Update everything
        action_manager.update(1 / 60.0)
        action_manager.draw_ui(resolution)

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
    #pygame.mixer.music.play()

    # Create screen
    global resolution
    resolution = pygame.display.set_mode((800, 480))
    resolution.fill('Green')

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
    
    # Create buttons
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (100, 50)), text='Play', manager=menu_manager)
    info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (100, 50)), text='Info', manager=menu_manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)), text='Quit', manager=menu_manager)

    # Initialize game state
    global deck
    deck = deck_func()
    deal_initial_cards(deck)

    print(f"Deck: {deck}")
    print(f"Stack: {deckcount}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED or event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == play_button:
                        print("Play button pressed")
                        first_deal_anim()
                        game_start()

                    elif event.ui_element == info_button:
                        print("Info button pressed")

                    elif event.ui_element == quit_button:
                        pygame.quit()
                        exit()

            menu_manager.process_events(event)

        # Draw all elements
        resolution.blit(ground, (0, 0))
        resolution.blit(card_deck, (10, 10))
        resolution.blit(titlecard_surface, (360, 185))
            
        # Update everything
        menu_manager.update(1 / 60.0)
        menu_manager.draw_ui(resolution)

        pygame.display.update()
        fps.tick(60)

if __name__ == "__main__":
    main()