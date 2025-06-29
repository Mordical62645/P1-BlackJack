import pygame
import pygame_gui
import random
import warnings

# Suppress libpng warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
CARD_START_POS = (10, 10)
PLAYER_Y = 250
DEALER_Y = 50
CARD_X_START = 250
CARD_X_GAP = 100
DECK_POS = (10, 10)
DECKPILE_POS = (700, 20)
BG_COLOR = (0, 128, 0)
FONT_PATH = "font/KarenFat.ttf"

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = None

    def load_image(self):
        if self.image is None:
            self.image = pygame.image.load(f"graphics/Cards/{self.value}{self.suit}.png")

    def __repr__(self):
        return f"{self.value}{self.suit}"

class Chips:
    def __init__(self, chipvalue, chipcolor):
        self.chipvalue = chipvalue
        self.chipcolor = chipcolor
        self.chipimage = None
    
    def load_image(self):
        if self.chipimage is None:
            self.chipimage = pygame.image.load(f"graphics/Chips/{self.chipvalue}{self.chipcolor}.png")

    def __repr__(self):
        return f"{self.chipvalue}{self.chipcolor}"

class BlackjackGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, int(SCREEN_HEIGHT * 0.06))
        self.deck_img = pygame.image.load("graphics/Card_Deck/card_deck.png")
        self.deckpile_img = pygame.image.load("graphics/Card_Deck/card_deckpileblank.png")
        self.bg_img = pygame.image.load("graphics/ground.jpg")
        self.drawing_sound = pygame.mixer.Sound("audio/sfx/drawing.mp3")
        self.dealing_sound = pygame.mixer.Sound("audio/sfx/dealing.mp3")
        self.channel = pygame.mixer.Channel(0)
        
        # Initialize background music
        pygame.mixer.music.load("audio/bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        
        # Initialize UI managers
        self.menu_manager = pygame_gui.UIManager((800, 480))
        self.betting_manager = pygame_gui.UIManager((800, 480))
        self.game_manager = pygame_gui.UIManager((800, 480))
        
        # Chip values dictionary
        self.chips_dict = {
            'Gray': 1,
            'Red': 5,
            'Blue': 10,
            'Yellow': 50,
            'Black': 100,
            'Violet': 500,
            'Orange': 1000
        }
        
        self.reset_game()

    def reset_game(self):
        self.deck = self.create_deck()
        self.discard_pile = []
        self.player_hand = []
        self.dealer_hand = []
        self.playerscore = []
        self.dealerscore = []
        self.dealer_card_targetx = CARD_X_START
        self.hit_targetx = CARD_X_START
        self.playertotal = 0
        self.dealertotal = 0
        self.state = 'title'  # title, betting, dealing, player_turn, dealer_turn, result
        self.result_message = ''
        self.bet = 0
        self.player_turn_over = False
        self.surrendered = False
        self.has_discarded_once = False
        self.has_discarded_once_already = False

    def create_deck(self):
        values = list(range(2, 11)) + ["J", "Q", "K", "A"]
        suits = ['h', 's', 'c', 'd']
        deck = [Card(value, suit) for suit in suits for value in values]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand, score, reveal=True):
        card = self.deck.pop()
        hand.append(card)
        value = self.get_card_value(card)
        score.append(value)
        if reveal:
            self.channel.play(self.dealing_sound)
        return card

    def get_card_value(self, card):
        if card.value in ["J", "Q", "K"]:
            return 10
        if card.value == "A":
            return 11
        return int(card.value)

    def animate_card(self, start_pos, end_pos, card_img):
        frames = 30
        for frame in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            t = frame / (frames - 1)
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
            self.draw_background()
            self.screen.blit(card_img, (x, y))
            self.draw_hands()
            pygame.display.flip()
            self.clock.tick(60)
        self.channel.play(self.drawing_sound)

    def draw_background(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.deck_img, DECK_POS)
        if self.has_discarded_once_already:
            self.screen.blit(self.deckpile_img, DECKPILE_POS)

    def draw_hands(self, hide_dealer_first=False):
        # Draw player cards
        for i, card in enumerate(self.player_hand):
            card.load_image()
            self.screen.blit(card.image, (CARD_X_START + i * CARD_X_GAP, PLAYER_Y))
        # Draw dealer cards
        for i, card in enumerate(self.dealer_hand):
            card.load_image()
            if i == 0 and hide_dealer_first:
                self.screen.blit(pygame.image.load("graphics/Card_Back/blind_card.png"), (CARD_X_START, DEALER_Y))
            else:
                self.screen.blit(card.image, (CARD_X_START + i * CARD_X_GAP, DEALER_Y))

    def show_result(self, message):
        self.result_message = message
        result_font = pygame.font.Font(FONT_PATH, int(SCREEN_HEIGHT * 0.08))
        result_surface = result_font.render(message, True, "Black")
        self.channel.play(self.dealing_sound)
        self.draw_background()
        self.draw_hands()
        self.screen.blit(result_surface, (SCREEN_WIDTH // 2 - result_surface.get_width() // 2, 200))
        pygame.display.flip()
        pygame.time.delay(2000)

    def deal_initial_cards(self):
        self.player_hand = []
        self.dealer_hand = []
        self.playerscore = []
        self.dealerscore = []
        self.dealer_card_targetx = CARD_X_START
        self.hit_targetx = CARD_X_START
        # Player 1
        self.animate_card(CARD_START_POS, (CARD_X_START, PLAYER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
        self.deal_card(self.player_hand, self.playerscore)
        # Dealer 1 (face down)
        self.animate_card(CARD_START_POS, (CARD_X_START, DEALER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
        self.deal_card(self.dealer_hand, self.dealerscore, reveal=False)
        # Player 2
        self.animate_card(CARD_START_POS, (CARD_X_START + CARD_X_GAP, PLAYER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
        self.deal_card(self.player_hand, self.playerscore)
        # Dealer 2 (face up)
        self.animate_card(CARD_START_POS, (CARD_X_START + CARD_X_GAP, DEALER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
        self.deal_card(self.dealer_hand, self.dealerscore)
        self.playertotal = sum(self.playerscore)
        self.dealertotal = sum(self.dealerscore)
        self.state = 'player_turn'
        self.player_turn_over = False
        self.surrendered = False

    def player_hit(self):
        self.animate_card(CARD_START_POS, (CARD_X_START + len(self.player_hand) * CARD_X_GAP, PLAYER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
        self.deal_card(self.player_hand, self.playerscore)
        self.playertotal = sum(self.playerscore)
        if self.playertotal > 21:
            self.player_turn_over = True
            self.state = 'dealer_turn'

    def player_stand(self):
        self.player_turn_over = True
        self.state = 'dealer_turn'

    def player_surrender(self):
        self.surrendered = True
        self.player_turn_over = True
        self.state = 'dealer_turn'

    def player_double(self):
        if len(self.player_hand) == 2:
            self.bet *= 2
            self.player_hit()
            self.player_turn_over = True
            self.state = 'dealer_turn'

    def dealer_play(self):
        # Reveal dealer's first card
        self.channel.play(self.dealing_sound)
        self.draw_background()
        self.draw_hands(hide_dealer_first=False)
        pygame.display.flip()
        pygame.time.delay(700)
        # Dealer draws to 17+
        self.dealertotal = sum(self.dealerscore)
        while self.dealertotal < 17:
            self.animate_card(CARD_START_POS, (CARD_X_START + len(self.dealer_hand) * CARD_X_GAP, DEALER_Y), pygame.image.load("graphics/Card_Back/blind_card.png"))
            self.deal_card(self.dealer_hand, self.dealerscore)
            self.dealertotal = sum(self.dealerscore)
        self.state = 'result'

    def determine_result(self):
        self.playertotal = sum(self.playerscore)
        self.dealertotal = sum(self.dealerscore)
        if self.surrendered:
            return "PLAYER SURRENDERS!"
        if self.playertotal > 21:
            return "PLAYER BUST! DEALER WINS!"
        if self.dealertotal > 21:
            return "DEALER BUST! PLAYER WINS!"
        if self.playertotal > self.dealertotal:
            return "PLAYER WINS!"
        if self.dealertotal > self.playertotal:
            return "DEALER WINS!"
        return "PUSH!"

    def discard_all(self):
        # Animate all cards to discard pile
        self.animate_discard_all()
        self.has_discarded_once = True
        self.has_discarded_once_already = True

    def animate_discard_all(self):
        # Gather all cards to move (player + dealer)
        cards_to_discard = []
        positions = []
        for i, c in enumerate(self.player_hand):
            c.load_image()
            cards_to_discard.append(c)
            positions.append((CARD_X_START + i * CARD_X_GAP, PLAYER_Y))
        for i, c in enumerate(self.dealer_hand):
            c.load_image()
            cards_to_discard.append(c)
            positions.append((CARD_X_START + i * CARD_X_GAP, DEALER_Y))

        # Animate all cards moving to DISCARD_POS at once
        frames = 30
        for frame in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            t = frame / (frames - 1)
            self.draw_background()
            # Draw all cards in transit
            for card, start_pos in zip(cards_to_discard, positions):
                x = start_pos[0] + (DECKPILE_POS[0] - start_pos[0]) * t
                y = start_pos[1] + (DECKPILE_POS[1] - start_pos[1]) * t
                self.screen.blit(card.image, (x, y))
            pygame.display.flip()
            self.clock.tick(60)

        # After animation, add to discard pile and clear hands
        self.discard_pile.extend(cards_to_discard)
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.playerscore.clear()
        self.dealerscore.clear()
        
        # Print discard pile information to terminal
        print(f"Discard pile count: {len(self.discard_pile)}")
        print(f"Discard pile cards: {[str(card) for card in self.discard_pile]}")
        print(f"Discard pile values: {[self.get_card_value(card) for card in self.discard_pile]}")
        
        # Print deck remaining information
        print(f"Cards remaining: {len(self.deck)}")
        print(f"Deck cards remaining: {[str(card) for card in self.deck]}")
        print(f"Deck card values remaining: {[self.get_card_value(card) for card in self.deck]}")
        
        pygame.time.delay(700)

    def can_continue_game(self):
        # Check if we have enough cards for another round (at least 10 cards)
        return len(self.deck) >= 10

    def reset_for_new_round(self):
        # Reset hands and scores for new round, but keep deck and discard pile
        self.player_hand = []
        self.dealer_hand = []
        self.playerscore = []
        self.dealerscore = []
        self.dealer_card_targetx = CARD_X_START
        self.hit_targetx = CARD_X_START
        self.playertotal = 0
        self.dealertotal = 0
        self.player_turn_over = False
        self.surrendered = False

    def create_title_screen(self):
        # Create title screen buttons
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (100, 50)), text='Play', manager=self.menu_manager)
        self.info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (100, 50)), text='Info', manager=self.menu_manager)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)), text='Quit', manager=self.menu_manager)

    def create_betting_screen(self):
        # Create betting buttons
        self.bet_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 400), (50, 50)), text='1', manager=self.betting_manager)
        self.bet_5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (50, 50)), text='5', manager=self.betting_manager)
        self.bet_10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (50, 50)), text='10', manager=self.betting_manager)
        self.bet_50 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 400), (50, 50)), text='50', manager=self.betting_manager)
        self.bet_100 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 400), (50, 50)), text='100', manager=self.betting_manager)
        self.bet_500 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 400), (50, 50)), text='500', manager=self.betting_manager)
        self.bet_1000 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 400), (50, 50)), text='1000', manager=self.betting_manager)
        self.bet_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 50), (50, 50)), text='Play', manager=self.betting_manager)

    def create_game_screen(self):
        # Create game action buttons
        self.hit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (100, 50)), text='Hit', manager=self.game_manager)
        self.stand_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 400), (100, 50)), text='Stand', manager=self.game_manager)
        self.surrender_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)), text='Surrender', manager=self.game_manager)
        self.double_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 400), (100, 50)), text='Double', manager=self.game_manager)
        self.split_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 400), (100, 50)), text='Split', manager=self.game_manager)

    def draw_chips(self):
        x = 60
        for color, value in self.chips_dict.items():
            chip = Chips(value, color)
            chip.load_image()
            if isinstance(chip.chipimage, pygame.Surface): 
                self.screen.blit(chip.chipimage, (x, 300))
                x += 100

    def run(self):
        self.create_title_screen()
        running = True
        
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle events based on current state
                if self.state == 'title':
                    self.menu_manager.process_events(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            self.state = 'betting'
                            self.create_betting_screen()
                        elif event.ui_element == self.info_button:
                            print("Info button pressed")
                        elif event.ui_element == self.quit_button:
                            running = False
                
                elif self.state == 'betting':
                    self.betting_manager.process_events(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.bet_1:
                            self.bet += 1
                        elif event.ui_element == self.bet_5:
                            self.bet += 5
                        elif event.ui_element == self.bet_10:
                            self.bet += 10
                        elif event.ui_element == self.bet_50:
                            self.bet += 50
                        elif event.ui_element == self.bet_100:
                            self.bet += 100
                        elif event.ui_element == self.bet_500:
                            self.bet += 500
                        elif event.ui_element == self.bet_1000:
                            self.bet += 1000
                        elif event.ui_element == self.bet_play:
                            if self.bet >= 500:
                                self.state = 'dealing'
                                self.create_game_screen()
                            else:
                                print("Bet must be 500 or above")
                
                elif self.state == 'player_turn':
                    self.game_manager.process_events(event)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.hit_button:
                            self.player_hit()
                        elif event.ui_element == self.stand_button:
                            self.player_stand()
                        elif event.ui_element == self.surrender_button:
                            self.player_surrender()
                        elif event.ui_element == self.double_button:
                            self.player_double()
                        elif event.ui_element == self.split_button:
                            print("Split functionality not implemented yet")
            
            # State machine rendering
            if self.state == 'title':
                self.draw_background()
                title_font = pygame.font.Font(FONT_PATH, int(SCREEN_HEIGHT * 0.08))
                title_surface = title_font.render("BlackJack", True, "Black")
                self.screen.blit(title_surface, (360, 185))
                self.menu_manager.update(time_delta)
                self.menu_manager.draw_ui(self.screen)
            
            elif self.state == 'betting':
                self.draw_background()
                self.draw_chips()
                bet_font = pygame.font.Font(FONT_PATH, int(SCREEN_HEIGHT * 0.06))
                bet_surface = bet_font.render(f"Bet: {self.bet}", True, "Black")
                self.screen.blit(bet_surface, (300, 185))
                self.betting_manager.update(time_delta)
                self.betting_manager.draw_ui(self.screen)
            
            elif self.state == 'dealing':
                self.deal_initial_cards()
            
            elif self.state == 'player_turn':
                self.draw_background()
                self.draw_hands(hide_dealer_first=True)
                self.game_manager.update(time_delta)
                self.game_manager.draw_ui(self.screen)
                if self.player_turn_over:
                    self.state = 'dealer_turn'
            
            elif self.state == 'dealer_turn':
                self.dealer_play()
            
            elif self.state == 'result':
                result = self.determine_result()
                self.show_result(result)
                self.discard_all()
                
                # Check if we can continue with another round
                if self.can_continue_game():
                    print(f"Starting new round. Cards remaining: {len(self.deck)}")
                    self.reset_for_new_round()
                    self.state = 'dealing'
                else:
                    print(f"Game over! Not enough cards remaining: {len(self.deck)}")
                    print("Returning to main menu...")
                    self.reset_game()
                    self.create_title_screen()
            
            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 480))
    pygame.display.set_caption("Blackjack Game")
    game = BlackjackGame(screen)
    game.run()
    pygame.quit() 