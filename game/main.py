##### LIBRARIES #####
import sys
import pygame
import pygame_gui
import random
import math

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

# Animation class for smooth card movements
class CardAnimation:
    def __init__(self, start_pos, end_pos, duration=0.5):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.completed = False
        
    def get_position(self, current_time):
        elapsed = (current_time - self.start_time) / 1000.0
        progress = min(elapsed / self.duration, 1.0)
        
        # Smooth easing function
        progress = self.ease_out_quad(progress)
        
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        
        if progress >= 1.0:
            self.completed = True
            
        return (x, y)
    
    def ease_out_quad(self, t):
        return t * (2 - t)

# Image cache for better performance
class ImageCache:
    def __init__(self):
        self.cache = {}
        
    def get_image(self, path):
        if path not in self.cache:
            self.cache[path] = pygame.image.load(path)
        return self.cache[path]

# Global image cache
image_cache = ImageCache()

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
    global deckcount, dealer_card_targetx
    
    if dealertotal <= 16:
        while dealertotal <= 16:
            channel1.play(sound1)

            deckcount -= 1
            
            dealer_card = deck.pop()
            dealerscore.append(deckvalues.pop())
            dealer_hand.append(dealer_card)
            
            dealertotal = sum(dealerscore)
            dealer_card_targetx += 100

            # Create smooth animation for dealer card
            animation = CardAnimation((10, 10), (dealer_card_targetx, 50), 0.3)
            current_time = pygame.time.get_ticks()
            
            while not animation.completed:
                current_time = pygame.time.get_ticks()
                pos = animation.get_position(current_time)
                
                # Draw background
                screen.blit(ground, (0, 0))
                screen.blit(card_deck, (10, 10))
                
                # Draw existing dealer cards
                for i, card in enumerate(dealer_hand[:-1]):
                    card.load_image() 
                    screen.blit(card.cardimage, (250 + i * 100, 50))
                
                # Draw animating card
                screen.blit(blind_card, pos)
                
                # Draw player cards
                for i, card in enumerate(player_hand):
                    card.load_image() 
                    screen.blit(card.cardimage, (250 + i * 100, 250))
                
                pygame.display.flip()
                fps.tick(60)

            print()
            print(f"Deck: {deck}")
            print(f"Deck values: {deckvalues}")
            print(f"Stack: {deckcount}")
            print(f"Dealer's hand: {dealer_hand} Score: {dealertotal}")
            print(f"Player's hand: {player_hand} Score: {playertotal}")

    pygame.time.delay(500)

    if len(dealer_hand) == 2:
        channel2.play(sound2) 

    return dealertotal, playertotal
    
def deal_initial_cards_animated(deck):
    global player_hand, dealer_hand, playerscore, dealerscore, playertotal, dealertotal, deckvalues, deckcount, blind_card

    player_hand = []
    dealer_hand = []
    playerscore = []
    dealerscore = []
    
    # Animation target positions
    player_positions = [(250, 250), (350, 250)]
    dealer_positions = [(250, 50), (350, 50)]
    sequence = [
        ('player', player_positions[0]),
        ('dealer', dealer_positions[0]),
        ('player', player_positions[1]),
        ('dealer', dealer_positions[1]),
    ]

    blind_card = image_cache.get_image("graphics/Card_Back/blind_card.png")
    drawing = "audio/sfx/drawing.mp3"
    sound1 = pygame.mixer.Sound(drawing)
    channel1 = pygame.mixer.Channel(0)
    channel1.set_volume(0.5)

    for idx, (who, pos) in enumerate(sequence):
        card = deck.pop()
        value = deckvalues.pop()
        deckcount -= 1

        # Animate the card as a blind card
        animation = CardAnimation((10, 10), pos, 0.4)
        channel1.play(sound1)
        while not animation.completed:
            current_time = pygame.time.get_ticks()
            anim_pos = animation.get_position(current_time)
            screen.blit(ground, (0, 0))
            screen.blit(card_deck, (10, 10))
            # Draw all cards already dealt (not including the one being animated)
            # For player
            for i in range(len(player_hand)):
                player_hand[i].load_image()
                screen.blit(player_hand[i].cardimage, player_positions[i])
            # For dealer
            for i in range(len(dealer_hand)):
                if i == 0:
                    screen.blit(blind_card, dealer_positions[i])
                else:
                    dealer_hand[i].load_image()
                    screen.blit(dealer_hand[i].cardimage, dealer_positions[i])
            # Draw animating card (as blind card) on top
            screen.blit(blind_card, anim_pos)
            pygame.display.flip()
            fps.tick(60)

        # After animation, add the card to the hand and draw all cards in their correct places
        if who == 'player':
            player_hand.append(card)
            playerscore.append(value)
        else:
            dealer_hand.append(card)
            dealerscore.append(value)

        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        for i, c in enumerate(player_hand):
            c.load_image()
            screen.blit(c.cardimage, player_positions[i])
        for i, c in enumerate(dealer_hand):
            if i == 0:
                screen.blit(blind_card, dealer_positions[i])
            else:
                c.load_image()
                screen.blit(c.cardimage, dealer_positions[i])
        pygame.display.flip()
        pygame.time.delay(100)  # Small pause for clarity

    playertotal = sum(playerscore) 
    dealertotal = sum(dealerscore) 

##### ACTION FUNCTIONS #####
def Hit_func(dealertotal, playertotal):
    global deckcount, hit_targetx, hit_targety

    player_card = deck.pop()
    playerscore.append(deckvalues.pop())
    player_hand.append(player_card)
    
    playertotal = sum(playerscore)
    dealertotal = sum(dealerscore)

    deckcount -= 1
    channel1.play(sound1)

    hit_targetx += 100  
    hit_targety = 250 

    # Create smooth animation for hit card
    animation = CardAnimation((10, 10), (hit_targetx, hit_targety), 0.4)
    current_time = pygame.time.get_ticks()
    
    while not animation.completed:
        current_time = pygame.time.get_ticks()
        pos = animation.get_position(current_time)

        # Draw background
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        
        # Draw dealer cards
        for i, card in enumerate(dealer_hand):
            card.load_image() 
            screen.blit(card.cardimage, (250 + i * 100, 50))
            if i == 1:
                screen.blit(blind_card, (250, 50))
        
        # Draw existing player cards
        for i, card in enumerate(player_hand[:-1]):
            card.load_image() 
            screen.blit(card.cardimage, (250 + i * 100, 250))
        
        # Draw animating card
        screen.blit(blind_card, pos)
        
        pygame.display.flip()
        fps.tick(60)

    print()
    print(f"Deck: {deck}")
    print(f"Deck values: {deckvalues}")
    print(f"Stack: {deckcount}")
    print(f"Player's hand: {player_hand} Score: {playertotal}")

    if playertotal > 21:        
        print("BUST!")
        # Show all dealer cards
        for i, card in enumerate(dealer_hand):
            card.load_image() 
            screen.blit(card.cardimage, (250 + i * 100, 50))
        
        # Show all player cards
        for i, card in enumerate(player_hand):
            card.load_image() 
            screen.blit(card.cardimage, (250 + i * 100, 250))

        pygame.display.flip()
        pygame.time.delay(2000)
        
        return dealertotal, playertotal

    return dealertotal, playertotal

def Stand_func(dealertotal, playertotal):    
    global deckcount, dealer_card_targetx
    
    # Reveal dealer's hidden card
    for i, card in enumerate(dealer_hand):
        card.load_image()
        screen.blit(card.cardimage, (250 + i * 100, 50))
    for i, card in enumerate(player_hand):
        card.load_image()
        screen.blit(card.cardimage, (250 + i * 100, 250))
    pygame.display.flip()
    pygame.time.delay(1000)
    
    # Dealer plays
    dealertotal, playertotal = dealer_dealing_cards(dealertotal, playertotal)

    # Reveal all dealer and player cards again (in case more were drawn)
    for i, card in enumerate(dealer_hand):
        card.load_image()
        screen.blit(card.cardimage, (250 + i * 100, 50))
    for i, card in enumerate(player_hand):
        card.load_image()
        screen.blit(card.cardimage, (250 + i * 100, 250))
    pygame.display.flip()
    pygame.time.delay(500)
    
    # Determine winner
    if dealertotal > 21:
        print("DEALER BUST! PLAYER WINS!")
        titlecard_surface = titlecard.render("DEALER BUST! PLAYER WINS!", False, "Black") 
        screen.blit(titlecard_surface, (200, 200))
    elif dealertotal > playertotal:
        print("DEALER WINS!")
        titlecard_surface = titlecard.render("DEALER WINS!", False, "Black") 
        screen.blit(titlecard_surface, (300, 200))
    elif playertotal > dealertotal:
        print("PLAYER WINS!")
        titlecard_surface = titlecard.render("PLAYER WINS!", False, "Black") 
        screen.blit(titlecard_surface, (300, 200))
    else:
        print("PUSH!")
        titlecard_surface = titlecard.render("PUSH!", False, "Black") 
        screen.blit(titlecard_surface, (350, 200))
    
    pygame.display.flip()
    pygame.time.delay(3000)
    
    # Animate discard all
    animate_discard_all()
    
    return dealertotal, playertotal

def Surrender_func(dealertotal, playertotal):
    print("PLAYER SURRENDERS!")
    titlecard_surface = titlecard.render("PLAYER SURRENDERS!", False, "Black") 
    screen.blit(titlecard_surface, (250, 200))
    pygame.display.flip()
    pygame.time.delay(2000)
    return dealertotal, playertotal

def Double_func():
    print("Double Down!")
    # Implement double down logic here
    pass

def Split_func():
    print("Split!")
    # Implement split logic here
    pass

def first_deal_anim():
    # Pre-load blind card image
    global blind_card
    blind_card = image_cache.get_image("graphics/Card_Back/blind_card.png")
    
    # Load sound
    global drawing, sound1, channel1
    drawing = "audio/sfx/drawing.mp3"
    sound1 = pygame.mixer.Sound(drawing)
    channel1 = pygame.mixer.Channel(0)
    channel1.set_volume(0.5)

    # Define card positions for initial deal
    card_positions = [
        (250, 50),   # Dealer first card
        (250, 250),  # Player first card
        (350, 50),   # Dealer second card
        (350, 250)   # Player second card
    ]
    
    # Create animations for each card
    animations = []
    for i, target_pos in enumerate(card_positions):
        animation = CardAnimation((10, 10), target_pos, 0.4)
        animations.append(animation)
    
    # Play all animations simultaneously
    start_time = pygame.time.get_ticks()
    completed = [False] * len(animations)
    
    while not all(completed):
        current_time = pygame.time.get_ticks()
        
        # Draw background
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        
        # Update and draw each animation
        for i, animation in enumerate(animations):
            if not completed[i]:
                pos = animation.get_position(current_time)
                screen.blit(blind_card, pos)
                completed[i] = animation.completed
                
                # Play sound for each card
                if not completed[i] and animation.get_position(current_time)[0] > 100:
                    channel1.play(sound1)
            
        pygame.display.flip()
        fps.tick(60)
    
    print("Initial deal complete!")

# Add global discard pile and position
discard_pile = []
DISCARD_POS = (700, 20)  # Top right corner
has_discarded_once = False

def animate_discard_all():
    global has_discarded_once
    # Gather all cards to move (player + dealer)
    cards_to_discard = []
    positions = []
    for i, c in enumerate(player_hand):
        c.load_image()
        cards_to_discard.append(c)
        positions.append((250 + i * 100, 250))
    for i, c in enumerate(dealer_hand):
        c.load_image()
        cards_to_discard.append(c)
        positions.append((250 + i * 100, 50))

    # Animate all cards moving to DISCARD_POS at once
    frames = 30
    for frame in range(frames):
        t = frame / (frames - 1)
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        if has_discarded_once or frame == frames - 1:
            screen.blit(card_deck, DISCARD_POS)
        # Draw all cards in transit
        for card, start_pos in zip(cards_to_discard, positions):
            x = start_pos[0] + (DISCARD_POS[0] - start_pos[0]) * t
            y = start_pos[1] + (DISCARD_POS[1] - start_pos[1]) * t
            screen.blit(card.cardimage, (x, y))
        pygame.display.flip()
        fps.tick(60)

    # After animation, add to discard pile and clear hands
    discard_pile.extend(cards_to_discard)
    player_hand.clear()
    dealer_hand.clear()
    playerscore.clear()
    dealerscore.clear()
    has_discarded_once = True
    print(f"Discard pile count: {len(discard_pile)}")
    print(f"Discard pile cards: {[str(card) for card in discard_pile]}")
    print(f"Discard pile values: {[card.cardvalue for card in discard_pile]}")

    # Automatically deal a new round if enough cards left
    if deckcount >= 10:  # or another threshold if you want
        deal_initial_cards_animated(deck)

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
    play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 50), (50, 50)), text='Play', manager=action_manager)
    
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
                        bet += 1
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_5:
                        bet += 5
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_10:
                        bet += 10
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_50:
                        bet += 50
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_100:
                        bet += 100
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_500:
                        bet += 500
                        print(f"Bet: {bet}")
                    elif event.ui_element == bet_1000:
                        bet += 1000
                        print(f"Bet: {bet}")
                    elif event.ui_element == play:
                        if bet <= 499:
                            pygame.time.delay(1000)
                            titlecard_surface = titlecard.render(f"Bet must be 500 above", False, "Black") 
                            screen.blit(titlecard_surface, (150, 225))
                        else:
                            return bet
                            
            action_manager.process_events(event)
        
        titlecard_surface = titlecard.render(f"Bet:{bet}", False, "Black") 
        screen.blit(titlecard_surface, (300, 185))

        # Update the UI
        action_manager.update(1 / 60)  # Assuming a 60 FPS game loop
        
        # Draw the UI
        action_manager.draw_ui(screen)
        
        # Update display and control frame rate
        pygame.display.flip()
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
    channel2.set_volume(0.5)
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
        
        # Draw background
        screen.blit(ground, (0, 0))
        screen.blit(card_deck, (10, 10))
        
        # Display player's cards
        for i, card in enumerate(player_hand):
            card.load_image()
            screen.blit(card.cardimage, (250 + i * 100, 250))

        # Display dealer's cards
        for i, card in enumerate(dealer_hand):
            card.load_image()    
            screen.blit(card.cardimage, (250 + i * 100, 50))

            if i == 1:
                screen.blit(blind_card, (250, 50))
        
        # Draw discard pile holder and count
        if has_discarded_once:
            screen.blit(card_deck, DISCARD_POS)

        # Update everything
        action_manager.update(1 / 60.0)
        action_manager.draw_ui(screen)

        pygame.display.flip()
        fps.tick(60)
              
##### MAIN #####
def main():
    global hit_targetx, dealer_card_targetx
    hit_targetx = 250
    dealer_card_targetx = 250
    
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("BlackJack - Optimized")

    # Initialize music
    pygame.mixer.music.load("audio/bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    # Initialize sound for card drawing (used in Hit, deal, etc)
    global sound1, channel1
    drawing = "audio/sfx/drawing.mp3"
    sound1 = pygame.mixer.Sound(drawing)
    channel1 = pygame.mixer.Channel(0)
    channel1.set_volume(0.5)

    # Create screen
    global screen
    screen = pygame.display.set_mode((800, 480))
    screen.fill('Green')

    global fps, titlecard
    fps = pygame.time.Clock()
    titlecard = pygame.font.Font("font/KarenFat.ttf", 50)

    # Pre-load images using cache
    global ground, titlecard_surface, card_deck
    ground = image_cache.get_image("graphics/ground.jpg")
    titlecard_surface = titlecard.render("BlackJack", False, "Black")
    card_deck = image_cache.get_image("graphics/Card_Deck/card_deck.png")

    # Initialize pygame_gui
    global menu_manager
    menu_manager = pygame_gui.UIManager((800, 480))
    
    # Initialize game state
    global deck
    deck = deck_func()
    deal_initial_cards_animated(deck)

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
                        bet = bet_start()
                        deal_initial_cards_animated(deck)
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

        pygame.display.flip()
        fps.tick(60)

if __name__ == "__main__":
    main()